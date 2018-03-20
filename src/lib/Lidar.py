"""."""
import os
import time
from logger import Logger
from rplidar import RPLidar


class Lidar:
    """."""

    def __init__(self):
        """."""
        os.system('sudo chmod 666 /dev/ttyUSB0')
        self.PORT_NAME = '/dev/ttyUSB0'

        file_path = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(file_path, os.pardir))
        file_path = os.path.abspath(os.path.join(file_path, "log.log"))
        self.log = Logger(file_path, logger_label="Lidar")

    def distance(self):
        """."""
        try:
            dist = float(self._measured_distance())
            self.log.log("distance() successful", level=3,
                         days_to_remain=1)
            return (dist)
        except:
            self.log.log("distance() exception", level=3, days_to_remain=1)
            self._measured_distance()

    def _measured_distance(self):
        """."""
        try:
            lidar = RPLidar(self.PORT_NAME)
            for measurment in lidar.iter_measurments():
                line = '\n'.join(str(v) for v in measurment)
                newline = line.split("\n")
                if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
                        (float(newline[2]) > 359.7 and
                         360 > float(newline[2]))):
                    distance = float(newline[3]) / 10
                    lidar.stop()
                    lidar.disconnect()
                    time.sleep(0.2)
                    break
            self.log.log("_measured_distance() successful", level=3,
                         days_to_remain=1)
            return (distance)
        except:
            self.log.log("_measured_distance() exception", level=3,
                         days_to_remain=1)
            lidar.disconnect()
            time.sleep(0.2)
            self._measured_distance()
