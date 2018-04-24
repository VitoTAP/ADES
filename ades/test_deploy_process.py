from unittest import TestCase


class TestDeployProcess(TestCase):


    def test_docker_run(self):
        from ades.docker_process import DockerRun
        process = DockerRun()
        process.submit_files()