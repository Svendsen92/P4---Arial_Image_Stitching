import os
import time
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

class lidar:
    
    def __init__(self):
        try:
            os.system('sudo chmod 666 /dev/ttyUSB0')
            return (True)
        except:
            return (False)

    def distance():
        _measuredDistance()
        return (dist)

                
    def _measuredDistance():
        lidar = RPLidar(PORT_NAME)
        for measurment in lidar.iter_measurments():
            line = '\n'.join(str(v) for v in measurment)
            newline = line.split("\n")
            if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
                (float(newline[2]) > 359.7 and 360 > float(newline[2]))):
                dist = float(newline[3]) / 10
                lidar.stop()
                lidar.disconnect()
                time.sleep(0.2)
                break

