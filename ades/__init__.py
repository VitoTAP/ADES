from flask import Flask
from pywps import Service
from .docker_generic import DockerProcessFiles
from .docker_process import DockerRun
from .deploy_process import DeployProcess
from flask import url_for,redirect

app = Flask(__name__)

deploy = DeployProcess()
processes = [DockerProcessFiles(), deploy]
mywps = [Service(processes, ['pywps.cfg'])]


@app.route('/' , methods=['GET'])
def root():
    return redirect(url_for('wps') + "?service=WPS&request=GetCapabilities")

@app.route('/deploy' , methods=['GET'])
def deploy():
    processes.append(DockerRun("newprocess"))
    mywps[0] =  Service(processes, ['pywps.cfg'])

@app.route('/wps' , methods=['GET', 'POST'])
def wps():
    return mywps[0]



if __name__ == '__main__':
    app.run()