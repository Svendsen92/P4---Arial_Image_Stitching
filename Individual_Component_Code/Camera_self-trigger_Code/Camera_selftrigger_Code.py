#!/usr/bin/env python

from rplidar import RPLidar
from sh import gphoto2 as gp
import Adafruit_BMP.BMP085 as BMP085 # This migth need to be BMP180
import signal, os, subprocess, datetime, time, logging



iteration = 0
shot_time = datetime.datetime.now().strftime("%Y-%m-%d %H: %M: %S")

# This is for the gphoto
clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
triggerCommand = ["--trigger-capture"] # Takes 5sec
triggerCommand2 = ["--capture-image"]  # takes 9sec
downloadCommand = ["--get-all-files"] # This gets/downloads all files # Takes 10 sec
downloadJPG_Command = ["--get-file=2"] # Takes 5sec
triggerAndDownload = ["--capture-image-and-download"] # Takes 12
pictureID = "Image No."
folder_name = shot_time
save_location = "/home/pi/Desktop/" + folder_name   # this is: "location you want to create the folder with the pictures in"

# This is for the data logging
logging.basicConfig(filename= shot_time,level=logging.DEBUG)

# This is for the BMP182
sensor = BMP085.BMP085()

# This is for the RPLidar
os.system('sudo chmod 666 /dev/ttyUSB0')
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

# Variables
Distance = 0
Angle = 0
iteration = 0
BMP_altitude = 0
previousBMP_altitude = 0
key = ""

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print ("Falied to create the new directory or One already exist")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand) # This executes the triggering of the camera
    time.sleep(3) # This is to take exposure time and such into account
    #gp(triggerCommand2)
    #gp(downloadCommand)
    gp(downloadJPG_Command)
    #gp(triggerAndDownload)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if (len(filename) < 13):    # This is to see if the image has been named after our convention
            if (filename.endswith(".JPG")):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print ("Renamed the JPG")
            elif (filename.endswith(".CR2")):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print ("Renamed the CR2")


info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)

try:
    for measurment in lidar.iter_measurments():
        line = '\n'.join(str(v) for v in measurment)
        newline = line.split("\n")
        BMP_altitude = sensor.read_altitude()
        
        if ((float(newline[2]) > 0 and 0.3 > float(newline[2])) or
            (float(newline[2]) > 359.7 and 360 > float(newline[2]))):
            #print ("Angle = " + newline[2])
            print ("Distance = " + newline[3])
            print ("Altitude = " + str(BMP_altitude) + '\n') 

            key = raw_input()
            #if ((abs(BMP_altitude - previousBMP_altitude) > 0.85) and (abs(BMP_altitude - previousBMP_altitude) < 1.15):
            if (key == "t"):
                killgphoto2Process()
                gp(clearCommand)
                createSaveFolder()
                captureImages()
                renameFiles(pictureID + str(iteration))
                logging.info('Image No.' + str (iteration) + '; Distance = ' + newline[3] + '; Altitude = ' +
                             str(BMP_altitude))
                iteration = iteration +1
                previousBMP_altitude = BMP_altitude
                
except key == "f":
    pass

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
