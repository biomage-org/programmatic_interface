import gzip
import shutil
import uuid

from biomage_programmatic_interface.s3_object import S3Object

class SampleFile(S3Object):
    def __init__(self, path):
        super().__init__(path)

        if not self.__is_compressed():
            self.__compress()

    @classmethod
    def from_sample_file(cls, sample_file):
        return SampleFile(sample_file.path())

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
            'sampleFileId': self._uuid,
            'size': self.size(),
            "metadata": {},
        }

    def __is_compressed(self):
        with gzip.open(self._path, 'r') as fh:
            try:
                # Try to read 1 byte of the file (Fails if not zipped)
                fh.read1()
                return True
            except:
                return False

    def __compress(self):
        with open(self._path, 'rb') as f_in:
            compressed_url = self._path + '.gz'
            with gzip.open(compressed_url, 'wb') as f_out:
                # Copying is done in chunks by default
                shutil.copyfileobj(f_in, f_out)
                self._path = compressed_url
