import os
import time
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
global dist

class lidar:
    
    def __init__():
        os.system('sudo chmod 666 /dev/ttyUSB0')

    def distance():
        _measuredDistance()
        if (dist > 0):
            return (dist)
        else:
            _measuredDistance()

def _measuredDistance():
    global dist
    try:
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
    except:
        lidar.disconnect()
        time.sleep(0.2)
        _measuredDistance()
