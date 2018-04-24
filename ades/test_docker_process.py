from unittest import TestCase

from flask.testing import FlaskClient
from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseResponse
from ades import app
import requests_mock
import requests
import json


class Response(BaseResponse):
    @cached_property
    def json(self):
        return json.loads(self.data)


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)

class TestDockerRun(TestCase):

    def setUp(self):

        app.testing = True
        app.response_class = Response
        app.test_client_class = TestClient
        self.app = app.test_client()

    def test_execute(self):
        with open("resources/executeDocker.xml","rb") as xml:
            result = self.app.post("wps", content_type="application_xml",data=xml)
            print(str(result.data))

    def test_docker_run(self):
        from ades.docker_process import DockerRun
        process = DockerRun()
        process.submit_files()

