#!/usr/bin/env python

import os
import math
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from rplidar import RPLidar

x = []
y = []
counter = 0

os.system('sudo chmod 666 /dev/ttyUSB0')
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)


for measurment in lidar.iter_measurments():
    line = '\n'.join(str(v) for v in measurment)
    newline = line.split("\n")

    theta = float(newline[2])
    distance = float(newline[3])
    if(distance > 0):        
        x_coord = math.cos(math.radians(theta)) * distance
        y_coord = math.sin(math.radians(theta)) * distance * -1
                        
        y.append(y_coord)
        x.append(x_coord)
            
        counter = counter +1
    if (counter == 1000):
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()

plt.plot(0, 0, 'ko')
plt.plot(x, y, 'ro')
plt.axis([-10000, 20000, -10000, 20000])
plt.show()


