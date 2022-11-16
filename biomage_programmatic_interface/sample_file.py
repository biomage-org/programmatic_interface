from os.path import getsize
import gzip
import shutil
import requests
import uuid

class SampleFile:
    def __init__(self, path):
        self.__path = path
        self.__uuid = str(uuid.uuid4())

    @classmethod
    def from_sample_file(cls, sample_file):
        return SampleFile(sample_file.path())

    def path(self):
        return self.__path

    def name(self):
        return self.__path.split('/')[-1]

    def uuid(self):
        return self.__uuid

    def folder(self):
        return self.__path.split('/')[-2]

    def size(self):
        return getsize(self.__path)

    def type(self): 
        file_types = {
            'matrix': 'matrix10x',
            'barcodes': 'barcodes10x',
            'features': 'features10x',
            'genes': 'features10x',
        }
        
        for file_type_key in file_types.keys():
            if file_type_key in self.name():
                return file_types[file_type_key]
        return None

    def to_json(self):
        return {
            'sampleFileId': self.__uuid,
            'size': self.size(),
        }

    def __is_compressed(self):
        with gzip.open(self.__path, 'r') as fh:
            try:
                # Try to read 1 byte of the file (Fails if not zipped)
                fh.read1()
                return True
            except:
                return False

    def compress(self):
        if self.__is_compressed():
            return

        with open(self.__path, 'rb') as f_in:
            compressed_url = self.__path + '.gz'
            with gzip.open(compressed_url, 'wb') as f_out:
                # Copying is done in chunks by default
                shutil.copyfileobj(f_in, f_out)
                self.__path = compressed_url

    def get_path(self):
        return self.__path