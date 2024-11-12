import pprint, logging

from UPISAS import get_response_for_get_request
from UPISAS.exemplar import Exemplar

pp = pprint.PrettyPrinter(indent=4)
logging.getLogger().setLevel(logging.INFO)


class Dingnet(Exemplar):
    """
    A class which encapsulates a self-adaptive exemplar run in a docker container.
    """
    def __init__(self, auto_start=False, container_name="dingnet"):
        docker_config = {
            "name":  container_name,
            "image": container_name,
            "ports": {3000: 3000},
            "environment": {
                "PORT": "3000"
            }
        }

        super().__init__("http://localhost:3000", docker_config, auto_start)

    def start_run(self):
        # self.exemplar_container.exec_run(cmd = f' sh -c "cd /usr/src/app && node {app}" ', detach=True)
        response = get_response_for_get_request("http://localhost:3000/start_run")
        if response.status_code != 200:
            print("Error starting simulation:", response.content.decode("utf-8"))
