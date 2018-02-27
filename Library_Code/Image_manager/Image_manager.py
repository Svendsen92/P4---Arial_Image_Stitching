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
    def init(picID, saveFolderPath):
        shot_date = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        pictureID = picID
        folder_name = shot_date
        save_location = saveFolderPath + folder_name   # this is: "location you want to create the folder with the pictures in"
        iteration = 0

    def takePicture():
        killgphoto2Process()
        gp(clearCommand)
        createSaveFolder()
        captureImages()
        renameFiles(pictureID + str(iteration))
        iteration = iteration +1


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
        print ("Falied to create the new directory or One already exist")
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
