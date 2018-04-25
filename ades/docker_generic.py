from docker.errors import ContainerError
from pywps import Process, LiteralInput, LiteralOutput, ComplexInput, ComplexOutput, Format
import json
from flask import jsonify
from .query_opensearch import get_products
from typing import Dict,List
import logging

class DockerProcessFiles(Process):

    def __init__(self):
        inputs = [
            LiteralInput('OpenSearchQuery', 'OpenSearchQuery', data_type='string'),
            LiteralInput('DockerImage', 'DockerImage', data_type='string'),
            LiteralInput('DockerRunCommand', 'Command', data_type='string',abstract="Command template to provide to docker run. The template will be evaluated for each entry returned by the OpenSearch query."),
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

    @property
    def log(self):
        try:
            return self._log
        except AttributeError:
            self._log = logging.root.getChild(
                self.__class__.__module__ + '.' + self.__class__.__name__
            )
            return self._log

    def _handler(self, request, response):
        query = request.inputs['OpenSearchQuery'][0].data
        image = request.inputs['DockerImage'][0].data
        command = request.inputs['DockerRunCommand'][0].data

        if 'DockerVolume' in request.inputs:
            volume = json.loads(request.inputs['DockerVolume'][0].data)

        mounts = None
        if 'DockerMount' in request.inputs:
            mounts = [json.loads(mount.data) for mount in request.inputs['DockerMount']]

        result = ["out1.tiff", "out2.tiff"]

        products = get_products(query)

        self.log.warning("Processing %d products", len(products))

        commands = DockerProcessFiles.get_commands(products,command)

        for c in commands:
            self.log.warning("Executing: %s", c)
            DockerProcessFiles.run_container(image,c,mounts)

        return response

    @staticmethod
    def get_commands(products:List,command_template:str)->List[str]:
        from string import Template
        cmd_template = Template(command_template)
        return [cmd_template.substitute(p) for p in products]

    @staticmethod
    def run_container(image, command, mounts):
        import docker
        client = docker.from_env()
        try:
            client.containers.run(image, command, mounts = mounts )
        except ContainerError as e:
            print(e.stderr)
            raise e
