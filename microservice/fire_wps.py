from flask import Flask
from pywps import Service
from flask import url_for,redirect

app = Flask(__name__)
from pywps import Process, LiteralInput, LiteralOutput,ComplexInput,ComplexOutput,Format


class DetectFire(Process):

    def __init__(self):
        inputs = [
            LiteralInput('filename','filename', data_type='string')
        ]
        outputs = [
            ComplexOutput(identifier='file_list',title='file list', supported_formats = [Format('JSON')])
        ]

        super().__init__(self._handler,'fire_detection','fire_detection',
            inputs=inputs,
            outputs=outputs
        )



    def _handler(self,request, response):
        filename = request.inputs['filename'][0].data
        import subprocess
        subprocess.run(["/opt/snap/bin/gpt", "-e", "/S1_Cal_Deb_ML_Spk_TC_cmd.xml",
                                                          "-Pinputdata=" + filename,
                                                          "-Poutputdata=/out/S1result"], stdout=subprocess.PIPE)
        return response


processes = [DetectFire() ]
mywps = Service(processes)


@app.route('/' , methods=['GET'])
def root():
    return redirect(url_for('wps') + "?service=WPS&request=GetCapabilities")


@app.route('/wps' , methods=['GET', 'POST'])
def wps():
    return mywps



if __name__ == '__main__':
    app.run()