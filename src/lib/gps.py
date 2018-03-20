"""."""
import os
from logger import Logger


class GPSReader:
    """."""

    def __init__(self):
        """."""
        self.position = {}

        file_path = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(file_path, os.pardir))
        file_path = os.path.abspath(os.path.join(file_path, "log.log"))
        self.log = Logger(file_path, logger_label="GPS")

    def get_position(self):
        """."""
        self.position['x'] = 4
        self.position['y'] = 5
        self.position['z'] = 2.5
        self.log.log("get_position() successfull", level=3, days_to_remain=1)
        return self.position
