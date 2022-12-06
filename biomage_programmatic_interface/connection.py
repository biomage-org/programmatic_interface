import boto3
import requests

import biomage_programmatic_interface.exceptions as exceptions
from biomage_programmatic_interface.experiment import Experiment


class Connection:
    def __init__(self, username, password, instance_url, verbose=True):
        self.verbose = verbose
        self.__api_url = self.__get_api_url(instance_url)
        cognito_params = self.__get_cognito_params().json()
        clientId = cognito_params["clientId"]
        region = cognito_params["clientRegion"]
        self.__authenticate(username, password, clientId, region)

    def __get_cognito_params(self):
        try:
            return requests.get(self.__api_url + "v2/programmaticInterfaceClient")
        except Exception:
            raise exceptions.InstanceNotFound() from None

    def __authenticate(self, username, password, clientId, region):
        client = boto3.client("cognito-idp", region_name=region)

        try:
            resp = client.initiate_auth(
                ClientId=clientId,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": username, "PASSWORD": password},
            )
        except Exception:
            raise exceptions.IncorrectCredentials() from None

        print("Authentication succesfull") if self.verbose else ""

        self.__jwt = resp["AuthenticationResult"]["IdToken"]

    def __get_api_url(self, instance_url):
        if instance_url == "local":
            return "http://localhost:3000/"
        if instance_url.startswith("https://"):
            return instance_url
        return f"https://api.{instance_url}/"

    def fetch_api(self, url, body = {}, method="POST"):
        methods = {
            'POST': requests.post, 
            'PATCH': requests.patch,
            'GET': requests.get,
            }

        headers = {
            "Authorization": "Bearer " + self.__jwt,
            "Content-Type": "application/json",
        }

        return methods[method](self.__api_url + url, json=body, headers=headers)

    def uploadS3(self, objectS3, signed_url, compress=True):
        if compress and not objectS3.is_compressed():
            objectS3.compress()
        headers = {"Content-type": "application/octet-stream"}
        with open(objectS3.path, "rb") as file:
            requests.put(signed_url, headers=headers, data=file.read())

        print(f"Uploaded {objectS3.path} to S3") if self.verbose else ""

    def create_experiment(self, experiment_name=None):
        experiment = Experiment.create_experiment(self, experiment_name)
        print(f"Experiment {experiment.name} created!") if self.verbose else ""
        return experiment

    def load_experiment(self, experiment_id):
        experiment = Experiment.load_experiment(self, experiment_id)
        print(f"Experiment {experiment.name} loaded!") if self.verbose else ""
        return experiment
