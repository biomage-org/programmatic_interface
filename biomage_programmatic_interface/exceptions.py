class InstanceNotFound(Exception):
    def __init__(self):
        super().__init__('The specified instance url does not exist')

class IncorrectCredentials(Exception):
    def __init__(self):
        super().__init__('Incorrect email or password')

class FileNotExists(Exception):
    def __init__(self, file_type):
        super().__init__(f'Requested file {file_type} does not exist')