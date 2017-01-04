import docker
import tarfile
from pathlib import Path
from io import BytesIO
from typing import List, Tuple



class Sandbox:

    def __init__(self, host_port=None):
        """
        we don't know docker client is thread-safe
        if Sandbox.docker_client is None:
            Sandbox.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        """

        IMG_SRC = "ajudgeteam/ajudge:base"
        DEFAULT_CONTAINER_PORT = 50000

        if host_port is None:
            raise Exception('host_port cannot be None. you must set it.')

        self.docker_client = docker.APIClient(base_url="unix://var/run/docker.sock")
        self.host_config = self.docker_client.create_host_config(port_bindings={DEFAULT_CONTAINER_PORT: host_port})
        self.container = self.docker_client.create_container(IMG_SRC, "/bin/bash", detach=True, tty=True,
                                                             ports=[DEFAULT_CONTAINER_PORT],
                                                             host_config=self.host_config)
        self.docker_client.start(container=self.container.get('Id'))

    def __del__(self):
        self.docker_client.stop(container=self.container.get('Id'))  # after 10 sec sigkill
        self.docker_client.wait(container=self.container.get('Id'))
        self.docker_client.remove_container(container=self.container.get('Id'))
        self.docker_client.close()
        del self.docker_client

    def exec(self, cmd: str) -> dict:
        # execute cmd in container
        wrapped_cmd = "bash -c \"" + cmd + "\""
        exec_id = self.docker_client.exec_create(self.container.get('Id'),
                                                 wrapped_cmd,
                                                 stderr=False)  # only stdout
        exec_output = self.docker_client.exec_start(exec_id)
        exec_info = self.docker_client.exec_inspect(exec_id)
        return {'Output': exec_output, 'ExitCode': exec_info.get('ExitCode')}

    # copy a file to sandbox
    # file_path : absolute path to a file
    # dest_path : path to a directory.
    #             absolute path or relative path (relative to root directory)
    def copy_file_to_sandbox(self, file_path: str, dest_path: str) -> bool:
        files = [] # file name, binary pair
        file_path = Path(file_path)
        if (not file_path.is_absolute()) or (not file_path.is_file()): # deny relative path or non-file
            raise FileNotFoundError # FIXME create proper exception

        file_obj = open(file_path, mode='rb') # reading in binary mode
        files.append((file_path.name, file_obj.read()))
        file_obj.close()

        return self.write_files_in_sandbox(files, dest_path)


    # write files in sandbox
    # dest_path : path to sandbox directory
    # files : list of (filename, bytes) pair
    def write_files_in_sandbox(self, files: List[Tuple[str, bytes]], dest_dir: str) -> bool:
        tar_file = BytesIO()  # use BytesIO to store tarfile in memory

        tarobj = tarfile.open(fileobj=tar_file, mode="w")
        for file_name, file_contents in files:
            tarinfo = tarfile.TarInfo(name=file_name) # set file name
            tarinfo.size = len(file_contents)  # set file size
            tarobj.addfile(tarinfo, BytesIO(file_contents))  # add file to archive

        tarobj.close()

        tar_file.seek(0)  # set stream position is start of the stream
        data = tar_file.read()
        return self.docker_client.put_archive(self.container.get('Id'), dest_dir, data)

    # get file from sandbox
    # file_path : A path to a file or a directory
    # For a directory, file_path should be end with '/' or '/.'
    # If path ends in /. then this indicates that only the contents of the path directory should be copied.
    # A symlink is always resolved to its target.
    def get_files_from_sandbox(self, file_path: str):
        res = [] # list of (filename, bytes) pair

        # Do we need to validate file_path?
        tar_data, stat_info = self.docker_client.get_archive(self.container.get('Id'), file_path)
        tar_data = tar_data.data # get data from HTTPresponse

        tar_stream = BytesIO(tar_data)
        tar_obj = tarfile.open(fileobj=tar_stream)
        for tar_info in tar_obj:
            if tar_info.isfile(): # only file
                # FIXME tar_info.name has additional charactor
                res.append((str(Path(tar_info.name).name), tar_obj.extractfile(tar_info).read()))
        return res
