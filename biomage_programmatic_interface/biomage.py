from biomage_programmatic_interface.connection import Connection
from biomage_programmatic_interface.experiment import Experiment
from biomage_programmatic_interface.plot import Plot

class Biomage:
    def __init__(self, connection, verbose=True):
        self.experiment = Experiment(connection, verbose)
        self.plot = Plot(connection)

    @staticmethod
    def authenticate(email, password, instance_url):
        connection = Connection(email, password, instance_url)
        return Biomage(connection)