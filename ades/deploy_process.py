
from pywps import Process, LiteralInput, LiteralOutput, ComplexInput, ComplexOutput, Format
import json
from flask import jsonify
from .docker_process import DockerRun


class DeployProcess(Process):

    def __init__(self):
        inputs = [
            LiteralInput('identifier', 'Process Identifier', data_type='string'),

        ]
        outputs = [
            LiteralOutput('status','status', data_type='string')
        ]

        super().__init__(self._handler, identifier="DeployProcess", title="DeployProcess",
                         inputs=inputs,
                         outputs=outputs
                         )

    def _handler(self, request, response):

        print(request)
        return response