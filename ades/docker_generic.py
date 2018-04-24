from docker.errors import ContainerError
from pywps import Process, LiteralInput, LiteralOutput, ComplexInput, ComplexOutput, Format
import json
from flask import jsonify


class DockerProcessFiles(Process):

    def __init__(self):
        inputs = [
            LiteralInput('OpenSearchQuery', 'OpenSearchQuery', data_type='string'),
            LiteralInput('DockerImage', 'DockerImage', data_type='string'),
            LiteralInput('DockerRunCommand', 'Command', data_type='string'),
            ComplexInput('DockerMount', 'DockerMount', supported_formats=[Format('JSON')],data_format=Format('JSON'), min_occurs=1,max_occurs=1000),
            ComplexInput('DockerVolume', 'DockerVolume', supported_formats=[Format('JSON')], min_occurs=0, max_occurs=1)
        ]
        outputs = [
            ComplexOutput('file_list','referenced output', supported_formats = [Format('JSON')])
        ]

        super().__init__(self._handler, identifier="DockerProcessFiles", title="DockerProcessFiles",
                         inputs=inputs,
                         outputs=outputs
                         )

    def _handler(self, request, response):
        query = request.inputs['OpenSearchQuery'][0].data
        image = request.inputs['DockerImage'][0].data
        command = request.inputs['DockerRunCommand'][0].data

        if 'DockerVolume' in request.inputs:
            volume = json.loads(request.inputs['DockerVolume'][0].data)

        if 'DockerMount' in request.inputs:
            mounts = [json.loads(mount.data) for mount in request.inputs['DockerMount']]

        result = ["out1.tiff", "out2.tiff"]

        DockerProcessFiles.run_container(image,command,mounts)

        return response

    @staticmethod
    def run_container(image, command, mounts):
        import docker
        client = docker.from_env()
        try:
            client.containers.run(image, command, mounts = mounts )
        except ContainerError as e:
            print(e.stderr)
            raise e
