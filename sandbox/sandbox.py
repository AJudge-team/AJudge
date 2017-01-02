import docker
import tarfile
import time
import os
from io import BytesIO


class Sandbox(object):

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

    def exec(self, cmd: str) -> dict:
        # execute cmd in container
        wrapped_cmd = "bash -c \"" + cmd + "\""
        exec_id = self.docker_client.exec_create(self.container.get('Id'),
                                                 wrapped_cmd,
                                                 stderr=False)  # only stdout
        exec_output = self.docker_client.exec_start(exec_id)
        exec_info = self.docker_client.exec_inspect(exec_id)
        return {'Output': exec_output, 'ExitCode': exec_info.get('ExitCode')}

    def copy_host_file_to_container(self, host_directory: str, container_directory: str) -> dict:
        cur_directory = os.path.dirname(__file__)  # find current absolute path
        os.chdir(cur_directory)

        try:
            source = open(host_directory).read()
        except FileNotFoundError:
            raise FileNotFoundError

        source = str.encode(source)  # convert str to bytes

        # extract file name in directory
        host_file_name = host_directory
        st = 0
        host_file_length = len(host_file_name)
        for i in range(0, host_file_length):
            if host_file_name[i] == '/':
                st = i + 1
        host_file_name = host_file_name[st:]

        return self.copy_host_to_container(
            source=source,
            container_directory=container_directory,
            container_file_name=host_file_name
        )

    def copy_host_to_container(self, source: bytes, container_directory: str, container_file_name: str) -> dict:
        data = BytesIO()  # in memory binary stream
        data_tar = tarfile.open(fileobj=data, mode="w")

        tarinfo = tarfile.TarInfo(name=container_file_name)
        tarinfo.size = len(source)  # source size in bytes

        data_tar.addfile(tarinfo, BytesIO(source))  # generate file with tarinfo, binary stream data
        data_tar.close()

        data.seek(0)  # set stream position is start of the stream

        return {'Success': self.docker_client.put_archive(
            container=self.container.get('Id'),
            path=container_directory,
            data=data
        ), 'Source': source}
