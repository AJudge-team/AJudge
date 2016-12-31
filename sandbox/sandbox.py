import docker

class Sandbox(object):

    def __init__(self):
        """
        we don't know docker client is thread-safe
        if Sandbox.docker_client is None:
            Sandbox.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        """
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.container = self.docker_client.create_container("ajudgeteam/ajudge:base","/bin/bash",detach=True,tty=True)
        self.docker_client.start(container=self.container.get('Id'))

    def __del__(self):
        self.docker_client.stop(container=self.container.get('Id')) # after 10 sec sigkill
        self.docker_client.wait(container=self.container.get('Id'))
        self.docker_client.remove_container(container=self.container.get('Id'))
        self.docker_client.close()


# execute cmd
    def exec(self, cmd):
        wrapped_cmd = "bash -c \"" + cmd + "\""
        exec_id = self.docker_client.exec_create(self.container.get('Id'),
                                                 wrapped_cmd,
                                                 stderr=False) # only stdout
        exec_output = self.docker_client.exec_start(exec_id)
        exec_info = self.docker_client.exec_inspect(exec_id)
        return {'Output' : exec_output, 'ExitCode' : exec_info.get('ExitCode')}