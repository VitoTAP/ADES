
from typing import List,Dict

def run_container(image:str, command:List[str], mounts:List[Dict]):
    import docker
    client = docker.from_env()
    from docker.errors import ContainerError
    try:
        client.containers.run(image, command, mounts=mounts)
    except ContainerError as e:
        print(e.stderr)
        raise e