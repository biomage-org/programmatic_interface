import datetime
import hashlib
from biomage_programmatic_interface.sample import Sample
from biomage_programmatic_interface.exceptions import *

class Experiment:
    def __init__(self, connection, verbose):
        self.connection = connection
        self.verbose = verbose

    def create_experiment(self):
        created_at = datetime.datetime.now().isoformat()
        hashed_string = hashlib.md5(created_at.encode())
        experiment_id = hashed_string.hexdigest()

        experiment_data = {
            'id': experiment_id,
            'name': experiment_id,
            'description': ''
        }
        
        response = self.connection.fetch_api('v2/experiments/' + experiment_id, json=experiment_data)

        print('Experiment {} created!'.format(experiment_id)) if self.verbose else ""
        return experiment_id

    def upload_samples(self, experiment_id, samples_path):
        samples = Sample.get_all_samples_from_path(samples_path)
        for sample in samples:
            try:
                self.__create_and_upload_sample(experiment_id, sample)
            except Exception:
                print('Upload failed. This is likely an error within the python package for uploading.')
                print('Please send an email to hello@biomage.net and we will try to resolve this problem as soon as possible.')

    def download_data(self, experiment_id, cell_sets = False):
        file_types = ['biomage-source','processed-matrix'] 
        if cell_sets:
            file_types.append('cell-sets')

        urls = [self.__get_data_url(experiment_id, file_type) for file_type in file_types] 
        print(urls)

    def __get_data_url(self, experiment_id, file_type):
        url_rds = f'v2/experiments/{experiment_id}/download/{file_type}'
        response = self.connection.fetch_api(url_rds, {}, 'GET')
        if response.status_code == 404:
            raise FileNotExists(file_type)

        return response.content

    def __notify_upload(self, experiment_id, sample_id, sample_file_type):
        url = "v2/experiments/{}/samples/{}/sampleFiles/{}".format(experiment_id, sample_id, sample_file_type)
        json = {  
            "uploadStatus": "uploaded"
        }
        response = self.connection.fetch_api(url, json, 'PATCH')

    def __create_sample_file(self, experiment_id, sample_uuid, sample_file):     
        url = 'v2/experiments/{}/samples/{}/sampleFiles/{}'.format(experiment_id, sample_uuid, sample_file.type())
        response = self.connection.fetch_api(url, sample_file.to_json())
        return response.content.decode('UTF-8')[1:-1]

    def __create_and_upload_sample(self, experiment_id, sample):
        url = 'v2/experiments/{}/samples/{}'.format(experiment_id, sample.uuid())
        self.connection.fetch_api(url, sample.to_json())

        print('Created sample {} - {}'.format(sample.name(), sample.uuid())) if self.verbose else ""

        for sample_file in sample.get_sample_files():
            s3url = self.__create_sample_file(experiment_id, sample.uuid(), sample_file)
            sample_file.compress()
            self.connection.upload_to_S3(s3url, sample_file.get_path())
            self.__notify_upload(experiment_id, sample.uuid(), sample_file.type())
            print('Uploaded {} - {}...'.format(sample_file.name(), sample_file.uuid())) if self.verbose else ""