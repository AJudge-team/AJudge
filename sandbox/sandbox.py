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
            raise Exception("host_port cannot be None. you must set it.")

        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
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
        return {"Output": exec_output, "ExitCode": exec_info.get('ExitCode')}

    def copy_file_to_container(self, host_directory: str, container_directory: str) -> dict:
        cur_directory = os.path.dirname(__file__)  # find absolute path
        os.chdir(cur_directory)

        data_tar_stream = BytesIO()  # in memory binary stream
        data_tar = tarfile.open(fileobj=data_tar_stream, mode="w")
        data = open(host_directory).read().encode("utf8")  # convert str to bytes

        tarinfo = tarfile.TarInfo(name="server.py")
        tarinfo.size = len(data)  # size in bytes

        data_tar.addfile(tarinfo, BytesIO(data))  # generate file with tarinfo, binary stream data
        data_tar.close()

        data_tar_stream.seek(0)  # set stream position is start of the stream

        return {"Success": self.docker_client.put_archive(
            container=self.container.get('Id'),
            path=container_directory,
            data=data_tar_stream
        ), "Bytes": data}

    def copy_bytes_to_container(self, source: bytes, container_directory: str, container_file_name: str) -> dict:
        data_tar_stream = BytesIO()  # in memory binary stream
        data_tar = tarfile.open(fileobj=data_tar_stream, mode="w")
        data = source

        tarinfo = tarfile.TarInfo(name=container_file_name)
        tarinfo.size = len(data)  # size in bytes

        data_tar.addfile(tarinfo, BytesIO(data))  # generate file with tarinfo, binary stream data
        data_tar.close()

        data_tar_stream.seek(0)  # set stream position is start of the stream

        return {"Success": self.docker_client.put_archive(
            container=self.container.get('Id'),
            path=container_directory,
            data=data_tar_stream
        ), "Bytes": data}
