""" 
This module does not take any arguments. It enables the use of an RPLidar using a breakout board to usb,
to be pluged into the raspberry pi's usb port. Furthermore it returns the distance measured to an 
object straigth ahead (through a narrow angel interval).
"""

import os
import time
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

class lidar:
    
    def __init__(self):
    	# This function sets the serialport mode to 666 which is necessary to make it work
        try:
            os.system('sudo chmod 666 /dev/ttyUSB0')
            return (True)
        except:
            return (False)

    def distance():
    	# This function returns the distance found by the _measuredDistance function
        _measuredDistance()
        return (dist)

                
def _measuredDistance():
	# This function assignates the distance, to an object in a narrow angle interval, to the dist variable 
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

