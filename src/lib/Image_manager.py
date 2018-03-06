import time
import cv2
from datetime import datetime
from sh import gphoto2 as gp
import signal
import os
import subprocess

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R",
                "--delete-all-files"]  # This deletes the images on the camera's SD-card
triggerAndDownload = ["--capture-image-and-download"]


class image_manager:

    def aquirePicture(picID, savePath, iteration):
        # This function calls all the necessary function to trigger, download,
        # create a folder, rename the image and iterates between each picture
        shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        pictureID = picID + str(iteration)
        folder_name = shot_time
        # this is: "location you want to create the folder with the pictures
        # in"
        save_location = savePath + folder_name
        image_path = save_location + "/" + pictureID

        _killgphoto2Process()
        try:
            gp(clearCommand)
            print("gp(clearCommand)")
            _createSaveFolder(save_location)
            print("_createSaveFolder(save_location)")
            _captureImages()
            print("_captureImages()")
            _renameFiles(pictureID)
            print("_renameFiles(pictureID)")
            if(_blurDetection(image_path) == "Blurry"):
                print("if(_blurDetection(image_path) == Blurry):")
                _deleteImage(image_path)
                print("_deleteImage(image_path)")
                return (False)
            else:
                return(True)
        except:
            print("Exception")
            return (False)


def _killgphoto2Process():
    # This function kills/terminates the process that is initiated when the
    # lidar is pluged in
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    # This searches for the line that the process we want to kill
    for line in out.splitlines():
        if (b'gvfsd-gphoto2' in line):   # This is the name of the process that we want to kill
            # kill the process
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def _createSaveFolder(newFolderPath):
    # This function creates a directory for the images to be stored in
    try:
        os.makedirs(newFolderPath)
    except:
        print("Falied to create the new directory or One already exist")
    os.chdir(newFolderPath)  # Directory already exists, so change to it


def _captureImages():
    # This function triggers the camera, downloads the picture that has been
    # taken and delete the picture on the camera
    gp(triggerAndDownload)
    gp(clearCommand)


def _renameFiles(newImageName):
    # This function renames the image to whatever protocol has been chosen
    for filename in os.listdir("."):
        if (len(filename) < 13):    # This is to see if the image has been named after our convention
            if (filename.endswith(".jpg")):
                os.rename(filename, (newImageName + ".jpg"))
            elif (filename.endswith(".cr2")):
                os.rename(filename, (newImageName + ".cr2"))


def _blurDetection(imagePath):
    # This function evaluates wether a image is burry or not
    blackPixel = 0
    whitePixel = 0
    src_image = cv2.imread(imagePath + ".jpg")
    median_image = cv2.medianBlur(src_image, 5)
    gray_image = cv2.cvtColor(median_image, cv2.COLOR_RGB2GRAY)
    adaptive_image = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    resized_image = cv2.resize(adaptive_image, (0, 0), fx=0.15, fy=0.15)
    # Goes to thourgh each pixel position
    for i in range(resized_image.shape[0]):
        for j in range(resized_image.shape[1]):
            # Evaluates the pixels' value
            if (resized_image[i, j] < 1):
                blackPixel = blackPixel + 1
            elif (resized_image[i, j] > 254):
                whitePixel = whitePixel + 1
    pixelRatio = blackPixel / whitePixel * 1000
    if (pixelRatio > 10):
        print("Not Blurred: " + str(pixelRatio))
        return ("Not Blurry")
    else:
        print("Blurred: " + str(pixelRatio))
        return ("Blurry")


def _deleteImage(imagePath):
    # This function deletes an image depending on the ID given
    os.remove(imagePath + ".jpg")
    os.remove(imagePath + ".cr2")
