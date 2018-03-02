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
from sh import gphoto2 as gp
import signal, os, subprocess

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
triggerCommand = ["--trigger-capture"] # "--image-capture" <-- this is an alternative
downloadCommand = ["--get-all-files"] # This gets/downloads all files
downloadJPG_Command = ["--get-file=2"]
triggerAndDownload = ["--capture-image-and-download"]

class Image_manager:
    def __init__(self, picID, savePath):  
        shot_date = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        pictureID = picID
        folder_name = shot_date
        save_location = savePath + folder_name   # this is: "location you want to create the folder with the pictures in"
        iteration = 0

    def aquirePicture():
        # This function calls all the necessary function to trigger, download, create a folder, rename the image and iterates between each picture
        try:
            _killgphoto2Process()
            gp(clearCommand)
            _createSaveFolder()
            _captureImages()
            _renameFiles(pictureID + str(iteration))
            
            if(_blurDetection(pictureID + str(iteration)) == "Blurry"):
                _deleteImage(pictureID + str(iteration))
                aquirePicture()
                
            iteration = iteration +1
            return (True) 
        except:
            return (False)            


def _killgphoto2Process():
    # This function kills/terminates the process that is initiated when the lidar is pluged in
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()
    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):   # This is the name of the process that we want to kill
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)    

def _createSaveFolder():
    # This function creates a directory for the images to be stored in
    try:
        os.makedirs(save_location)
    except:
        os.chdir(save_location) # Directory already exists, so change to it 

def _captureImages():
    # This function triggers the camera, downloads the picture that has been taken and delete the picture on the camera
    gp(triggerCommand)      
    time.sleep(3)           # This is to take exposure time and such into account
    gp(downloadJPG_Command) 
    gp(clearCommand)

def _renameFiles(ID):
    # This function renames the image to whatever protocol has been chosen
    for filename in os.listdir("."):
        if (len(filename) < 13):    # This is to see if the image has been named after our convention
            if (filename.endswith(".JPG")):
                os.rename(filename, (shot_time + ID + ".JPG"))
            elif (filename.endswith(".CR2")):
                os.rename(filename, (shot_time + ID + ".CR2"))


def _blurDetection(ID):
    # This function evaluates wether a image is burry or not
    blackPixel = 0
    whitePixel = 0
    
    src_image = cv2.imread(save_location + shot_time + ID + ".JPG")
    median_image = cv2.medianBlur(src_image,5) 
    gray_image = cv2.cvtColor(median_image, cv2.COLOR_RGB2GRAY)
    adaptive_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    resized_image = cv2.resize(adaptive_image, (0,0), fx=0.15, fy=0.15)

    # Goes to thourgh each pixel position
    for i in range(resized_image.shape[0]):
        for j in range(resized_image.shape[1]):
            # Evaluates the pixels' value
            if (resized_image[i,j] < 1):
                blackPixel = blackPixel +1   
            elif (resized_image[i,j] > 254):
                whitePixel = whitePixel +1
    pixelRatio = blackPixel / whitePixel * 1000
    if (pixelRatio > 19):
        return ("Not Blurry")
    else:
        return ("Blurry")

def _deleteImage(ID):
    # This function deletes an image depending on the ID given
    os.remove(save_location + shot_time + ID + ".JPG")
    


