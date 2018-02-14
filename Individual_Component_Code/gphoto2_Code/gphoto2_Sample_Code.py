import time
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# This is to kill the process that starts evertime the camera is connected
def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout = subprocess.PIPE)
    out, err = p.communicate()

    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):   # This is the name of the process that we want to kill
            #kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


iteration = 0

shot_date = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
pictureID = "project No."

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]  # This deletes the images on the camera's SD-card       
triggerCommand = ["--trigger-capture"] # "--image-capture" <-- this is an alternative
downloadCommand = ["--get-all-files"]
triggerAndDownload = ["--capture-image-and-download"]

folder_name = shot_date
save_location = "/home/pi/Desktop/P4_Project/gPhoto2/gphoto_pics/" + folder_name   # this is: "location you want to create the folder with the pictures in"

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print ("Falied to create the new directory or One already exist")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand) # This executes the triggering of the camera
    time.sleep(3) # This is to take exposure time and such into account
    gp(downloadCommand)
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

totalTime = time.time()

for i in range(0,5):
    time1 = time.time()

    killgphoto2Process()
    gp(clearCommand)
    createSaveFolder()
    captureImages()
    renameFiles(pictureID + str(iteration))
    iteration = iteration +1
    
    time2 = time.time()
    print ("Execution time = " + str(time2 - time1))
    
endTime = time.time()
print ("Total time =" + str(endTime - totalTime))











                






