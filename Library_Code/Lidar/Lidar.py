import os
import time
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

class Lidar():
    def init():
        os.system('sudo chmod 666 /dev/ttyUSB0')
        lidar = RPLidar(PORT_NAME)

    def measuredDistance():
        for measurment in lidar.iter_measurments():
            line = '\n'.join(str(v) for v in measurment)
            newline = line.split("\n")
            
            if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
                (float(newline[2]) > 359.7 and 360 > float(newline[2]))):
                return (float(newline[3]))

    def exit():
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
