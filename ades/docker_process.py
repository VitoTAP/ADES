from docker.errors import ContainerError
from pywps import Process, LiteralInput, LiteralOutput,ComplexInput,ComplexOutput,Format


class DockerRun(Process):


    args=["--input","${input.filename}"]


    def __init__(self,identifier,image = "ogc/eoephackaton"):
        inputs = [
            LiteralInput('OpenSearchQuery','OpenSearchQuery', data_type='string')
        ]
        outputs = [
            ComplexOutput(identifier='file_list',title='file list', supported_formats = [Format('JSON')])
        ]
        self.image = image

        super().__init__(self._handler,identifier,identifier,
            inputs=inputs,
            outputs=outputs
        )



    def _handler(self,request, response):
        query = request.inputs['OpenSearchQuery'][0].data
        print("processing query:" + query)
        self.submit_files() 
        return response


    def submit_files(self):
        import docker
        client = docker.from_env()
        try:
            client.containers.run(self.image, ["/opt/snap/bin/gpt", "-e", "/S1_Cal_Deb_ML_Spk_TC_cmd.xml",
                                                          "-Pinputdata=/eodata/Sentinel-1/SAR/SLC/2017/06/17/S1A_IW_SLC__1SDV_20170617T064400_20170617T064430_017070_01C718_E903.SAFE",
                                                          "-Poutputdata=/out/S1result"],
                                  volumes={'/eodata': {'bind': '/eodata', 'mode': 'ro'},
                                           '/tmp': {'bind': '/out', 'mode': 'rw'},
                                           '/DEM': {'bind': '/DEM', 'mode': 'rw'}
                                          })
        except ContainerError as e:
            print(e.stderr)
