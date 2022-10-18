import boto3
import requests
import datetime
import hashlib
import requests
import datetime
import re
from biomage_programmatic_interface.s3_object import S3Object
from biomage_programmatic_interface.sample import Sample
from biomage_programmatic_interface.utils import load_json

class Connection:
    def __init__(self, username, password):
        self.__cognito_config = load_json('cognito.config.json')
        self.__default_config = load_json('default.config.json')
        self.__try_authenticate(username, password)

    def __try_authenticate(self, username, password):
        client = boto3.client('cognito-idp')

        try:
            resp = client.initiate_auth(
                ClientId=self.__cognito_config['ClientId'],
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters = { 
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )

            print('Authorization succesfull')
            self.__jwt = resp['AuthenticationResult']['IdToken']
            print(self.__jwt)
        except:
            raise Exception("Incorrect username or password")

    def __fetch_api(self, url, json, method='POST'):
        methods = {
            'POST': requests.post,
            'PATCH': requests.patch,
            'GET': requests.get
        }

        root_url = self.__default_config['api-url']
        headers = {
            'Authorization': 'Bearer ' + self.__jwt,
            'Content-Type': 'application/json'
        }

        return methods[method](root_url + url, json=json, headers=headers)

    def create_experiment(self):
        created_at = datetime.datetime.now().isoformat()
        hashed_string = hashlib.md5(created_at.encode())
        experiment_id = hashed_string.hexdigest()

        experiment_data = {
            'id': experiment_id,
            'name': experiment_id,
            'description': ''
        }

        response = self.__fetch_api('v2/experiments/' + experiment_id, json=experiment_data)

        print('Experiment {} created!'.format(experiment_id))
        return experiment_id

    def __notify_upload(self, experiment_id, sample_id, sample_file_type):
        url = "v2/experiments/{}/samples/{}/sampleFiles/{}".format(experiment_id, sample_id, sample_file_type)
        json = {  
            "uploadStatus": "uploaded"
        }
        response = self.__fetch_api(url, json, 'PATCH')

    def __create_sample_file(self, experiment_id, sample_uuid, sample_file):     
        url = 'v2/experiments/{}/samples/{}/sampleFiles/{}'.format(experiment_id, sample_uuid, sample_file.type())
        response = self.__fetch_api(url, sample_file.to_json())
        return response.content

    def __create_and_upload_sample(self, experiment_id, sample):
        url = 'v2/experiments/{}/samples/{}'.format(experiment_id, sample.uuid())
        self.__fetch_api(url, sample.to_json())

        print('Created sample {} - {}'.format(sample.name(), sample.uuid()))

        for sample_file in sample.get_sample_files():
            s3url_raw = self.__create_sample_file(experiment_id, sample.uuid(), sample_file)
            s3url = re.search(r"b\'\"(.*)\"\'", str(s3url_raw)).group(1)
            sample_file.upload_to_S3(s3url)
            self.__notify_upload(experiment_id, sample.uuid(), sample_file.type())
            print('Uploaded {} - {}...'.format(sample_file.name(), sample_file.uuid()))

    def upload_samples(self, experiment_id, samples_path):
        samples = Sample.get_all_samples_from_path(samples_path)
        for sample in samples:
            self.__create_and_upload_sample(experiment_id, sample)

        print('Project successfully created!')
        print('Visit {} to process your project.'.format(self.__default_config['ui-url']))

    def upload_experiment_results(self, experiment_id, img_path):
        s3Url = self.__fetch_api('v2/uploadExperimentResults/{}'.format(experiment_id), 'GET')
        
        s3Object = S3Object(img_path)
        s3Object.upload_to_S3(s3Url)