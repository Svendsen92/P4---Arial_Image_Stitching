#!/usr/bin/env python

import os
#import sys
#import glob
import time
from rplidar import RPLidar

os.system('sudo chmod 666 /dev/ttyUSB0')

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

global Distance
Distance = 0
global Angle
Angle = 0
global counter
counter = 0

info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)
time1 = time.time()
for measurment in lidar.iter_measurments():
    line = '\n'.join(str(v) for v in measurment)
    newline = line.split("\n")
    
    #print ("State = " + newline[0])
    #print ("Quality = " + newline[1])
    #print ("Angle = " + newline[2])
    #print ("Distance = " + newline[3])
    
    if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
        (float(newline[2]) > 359.7 and 360 > float(newline[2]))):
        print ("Angle = " + newline[2])
        print ("Distance = " + newline[3] + '\n')
        
        counter = counter +1

    if (counter == 50):
        break
time2 = time.time()

print ("time = " + str(time2 - time1))

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
