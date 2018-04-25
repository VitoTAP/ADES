from unittest import TestCase

from flask.testing import FlaskClient
from werkzeug.utils import cached_property
from werkzeug.wrappers import BaseResponse
from ades import app
import requests_mock
import requests
import json
from ades.docker_generic import DockerProcessFiles
from .query_opensearch import get_products

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

    def test_command_templates(self):


        #products = get_products("properties.beginposition:[2018-04-01 TO 2018-04-10] AND properties.orbitdirection:DESCENDING AND properties.platformname:Sentinel-1 AND properties.producttype:SLC")
        with open("resources/S1_product.json") as productfile:
            products = [json.load(productfile)]
        print(products)
        template = '/opt/snap/bin/gpt -e "/S1_Cal_Deb_ML_Spk_TC_cmd.xml" "-Pinputdata=$local_filename" "-Poutputdata=/out/S1result"'
        commands = DockerProcessFiles.get_commands(products[0:1],template)
        print(commands)
        self.assertEqual('/opt/snap/bin/gpt -e "/S1_Cal_Deb_ML_Spk_TC_cmd.xml" "-Pinputdata=/data/CGS_S1_SLC_L1/IW/DV/2018/04/01/S1B_IW_SLC__1SDV_20180401T055805_20180401T055832_010286_012B58_B59B/S1B_IW_SLC__1SDV_20180401T055805_20180401T055832_010286_012B58_B59B.zip" "-Poutputdata=/out/S1result"',commands[0])

    def test_docker_run(self):
        from ades.docker_process import DockerRun
        process = DockerRun()
        process.submit_files()


