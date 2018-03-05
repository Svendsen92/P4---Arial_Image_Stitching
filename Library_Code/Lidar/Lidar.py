import os
import time
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

class lidar:
    
    def __init__():
        os.system('sudo chmod 666 /dev/ttyUSB0')

    def distance():
        try:
            dist = float(_measuredDistance())
            return (dist)
        except:
            _measureDistance()
       
def _measuredDistance():
    try:
        lidar = RPLidar(PORT_NAME)
        for measurment in lidar.iter_measurments():
            line = '\n'.join(str(v) for v in measurment)
            newline = line.split("\n")
            if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
                (float(newline[2]) > 359.7 and 360 > float(newline[2]))):
                distance = float(newline[3]) / 10
                lidar.stop()
                lidar.disconnect()
                time.sleep(0.2)
                break
        return (distance)
    except:
        lidar.disconnect()
        time.sleep(0.2)
        _measuredDistance()
