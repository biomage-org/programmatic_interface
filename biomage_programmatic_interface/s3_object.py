import uuid
from os.path import getsize
import requests

class S3Object:
    def __init__(self, path):
        self._path = path
        self._uuid = str(uuid.uuid4())

    def path(self):
        return self._path

    def name(self):
        return self._path.split('/')[-1]

    def uuid(self):
        return self._uuid

    def folder(self):
        return self._path.split('/')[-2]

    def size(self):
        return getsize(self._path)

    def upload_to_S3(self, signed_url):
        headers = { 'Content-type': 'application/octet-stream' }
        with open(self._path, 'rb') as file:
            response = requests.put(signed_url, headers = headers, data = file.read())