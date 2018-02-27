"""
This class has two public functions. The first is the init() function it takes two arguments,
1) A string that gives the picture an id,
2) A string that contains the path to the folder where pictures are to be stored.
The init() function sets up the envioriment needed to execute the second function.

The second function is aquirePicture(), it does not take any arguments because everything
already has been set up by the init() function. takePicture() delete all pictures in
this folder "/store_00020001/DCIM/100CANON" on the camera, then it creates a folder at the specified
location (specified in the init() function) unless there already is a folder there with the same name.
It then takes the picture and downloads it to the created folder and thereafter the picture is renamed
in acoordance with the specified pictureID (specified in the init() function). 
"""

import time
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
triggerCommand = ["--trigger-capture"] # "--image-capture" <-- this is an alternative
downloadCommand = ["--get-all-files"] # This gets/downloads all files
downloadJPG_Command = ["--get-file=2"]
triggerAndDownload = ["--capture-image-and-download"]


################## Image_manager class ########################
class Image_manager():
    
    def init(picID, savePath):
        shot_date = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        pictureID = picID
        folder_name = shot_date
        save_location = savePath + folder_name   # this is: "location you want to create the folder with the pictures in"
        iteration = 0

    def aquirePicture():
        try:
            killgphoto2Process()
            gp(clearCommand)
            createSaveFolder()
            captureImages()
            renameFiles(pictureID + str(iteration))
            iteration = iteration +1
            return (True) 
        except:
            return (False)            


################## Image_manager script #########################
def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()
    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):   # This is the name of the process that we want to kill
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)    

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        #print ("Falied to create the new directory or One already exist")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)      
    time.sleep(3)           # This is to take exposure time and such into account
    gp(downloadJPG_Command) 
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if (len(filename) < 13):    # This is to see if the image has been named after our convention
            if (filename.endswith(".JPG")):
                os.rename(filename, (shot_time + ID + ".JPG"))
                #print ("Renamed the JPG")
            elif (filename.endswith(".CR2")):
                os.rename(filename, (shot_time + ID + ".CR2"))
                #print ("Renamed the CR2")
