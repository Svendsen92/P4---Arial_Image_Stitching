from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# This is to kill the process that starts evertime the camera is connected
def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()

    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
pictureID = "projectShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
triggerCommand = ["--trigger-capture"] # "--image-capture" <-- this is an alternative
downloadCommand = ["--get-all-files"]

folder_name = shot_date + pictureID
save_location = "/home/pi/Desktop/P4_Project/gPhoto2/gphoto_pics/" + folder_name   # this is: "location you want to create the folder with the pictures in"

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print ("Falied to create the new directory")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand) # This executes the triggering of the camera
    sleep(3) # This is to take exposure time and such into account
    gp(downloadCommand)
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
            


killgphoto2Process()
gp(clearCommand)
createSaveFolder()
captureImages()
renameFiles(pictureID)
















                






