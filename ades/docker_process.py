from docker.errors import ContainerError
from pywps import Process, LiteralInput, LiteralOutput,ComplexInput,ComplexOutput,Format


class DockerRun(Process):


    args=["--input","${input.filename}"]


    def __init__(self,identifier,image = "ogc/snapimage"):
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
        pass


    def submit_files(self):
        import docker
        client = docker.from_env()
        try:
            client.containers.run(self.image, ["/opt/snap/bin/gpt", "-e", "/S1_Cal_Deb_ML_Spk_TC_cmd.xml",
                                                          "-Pinputdata=/data/CGS_S1_SLC_L1/IW/DV/2018/02/17/S1B_IW_SLC__1SDV_20180217T060533_20180217T060600_009659_0116BD_A58F/S1B_IW_SLC__1SDV_20180217T060533_20180217T060600_009659_0116BD_A58F.zip",
                                                          "-Poutputdata=/out/S1result"],
                                  volumes={'/home/driesj/alldata/CGS_S1': {'bind': '/data', 'mode': 'ro'},
                                           '/tmp': {'bind': '/out', 'mode': 'rw'}})
        except ContainerError as e:
            print(e.stderr)
