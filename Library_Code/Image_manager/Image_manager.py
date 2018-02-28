"""
This module has two public functions. The first is the init() function it takes two arguments,
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
from sh import gphoto2 as _gp
import signal, os, subprocess

_clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
_triggerCommand = ["--trigger-capture"] # "--image-capture" <-- this is an alternative
_downloadCommand = ["--get-all-files"] # This gets/downloads all files
_downloadJPG_Command = ["--get-file=2"]
_triggerAndDownload = ["--capture-image-and-download"]

    
def init(picID, savePath):
    shot_date = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
    shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
    pictureID = picID
    folder_name = shot_date
    save_location = savePath + folder_name   # this is: "location you want to create the folder with the pictures in"
    iteration = 0

def aquirePicture():
    try:
        _killgphoto2Process()
        _gp(_clearCommand)
        _createSaveFolder()
        _captureImages()
        _renameFiles(pictureID + str(iteration))
        iteration = iteration +1
        return (True) 
    except:
        return (False)            

def _killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()
    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):   # This is the name of the process that we want to kill
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)    

def _createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
    os.chdir(save_location) # Directory already exists 

def _captureImages():
    _gp(_triggerCommand)      
    time.sleep(3)           # This is to take exposure time and such into account
    _gp(_downloadJPG_Command) 
    _gp(_clearCommand)

def _renameFiles(ID):
    for filename in os.listdir("."):
        if (len(filename) < 13):    # This is to see if the image has been named after our convention
            if (filename.endswith(".JPG")):
                os.rename(filename, (shot_time + ID + ".JPG"))
            elif (filename.endswith(".CR2")):
                os.rename(filename, (shot_time + ID + ".CR2"))
