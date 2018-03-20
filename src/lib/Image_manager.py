"""."""
import cv2
from datetime import datetime
from sh import gphoto2 as gp
import signal
import os
import subprocess
from logger import Logger


class ImageManager:
    """."""

    def __init__(self):
        """."""
        file_path = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(file_path, os.pardir))
        file_path = os.path.abspath(os.path.join(file_path, "log.log"))
        self.log = Logger(file_path, logger_label="Image_manager")

        # This deletes the images on the camera's SD-card
        self.clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", "-R",
                             "--delete-all-files"]
        self.triggerAndDownload = ["--capture-image-and-download"]

    def aquire_picture(self, pic_id, save_path, iteration):
        """."""
        # This function calls all the necessary function to trigger, download,
        # create a folder, rename the image and iterates between each picture
        shot_time = datetime.now().strftime("%Y-%m-%d %H: %M: %S")
        picture_id = pic_id + str(iteration)
        folder_name = shot_time
        # this is: "location you want to create the folder with the pictures
        # in"
        save_location = save_path + folder_name
        image_path = save_location + "/" + picture_id
        message = {"status": False, "name": image_path}

        self._kill_gphoto2_process()
        try:
            gp(self.clearCommand)
            self.log.log("gp(clearCommand)", level=3, days_to_remain=1)
            self._create_save_folder(save_location)
            self.log.log("_create_save_folder(save_location)", level=3,
                         days_to_remain=1)
            self._capture_images()
            self.log.log("_capture_images()", level=3, days_to_remain=1)
            self._rename_files(picture_id)
            self.log.log("_rename_files(picture_id)", level=3,
                         days_to_remain=1)
            if(self._blur_detection(image_path) == "Blurry"):
                self.log.log("if(_blur_detection(image_path) == Blurry):",
                             level=3, days_to_remain=1)
                self._delete_image(image_path)
                self.log.log("_delete_image(image_path)", level=3,
                             days_to_remain=1)
                return message
            else:
                message["status"] = True
                self.log.log("Image Aquired Successfully", level=3,
                             days_to_remain=1)
                return message
        except:
            self.log.log("Image aquire exception",
                         level=3, days_to_remain=1)
            return message

    def _kill_gphoto2_process():
        """."""
        # This function kills/terminates the process that is initiated when the
        # lidar is pluged in
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        # This searches for the line that the process we want to kill
        for line in out.splitlines():
            # This is the name of the process that we want to kill
            if (b'gvfsd-gphoto2' in line):
                # kill the process
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def _create_save_folder(self, new_folder_path):
        """."""
        # This function creates a directory for the images to be stored in
        try:
            os.makedirs(new_folder_path)
        except:
            self.log.log("_create_save_folder exception", level=3,
                         days_to_remain=1)
            # Directory already exists so change to it
            os.chdir(new_folder_path)

    def _capture_images(self):
        """
        Capture images.

        This function triggers the camera, downloads the picture that has been
        taken and delete the picture on the camera.
        """
        gp(self.triggerAndDownload)
        gp(self.clearCommand)

    def _rename_files(self, new_image_name):
        """."""
        # This function renames the image to whatever protocol has been chosen
        for filename in os.listdir("."):
            # This is to see if the image has been named after our convention
            if (len(filename) < 13):
                if (filename.endswith(".jpg")):
                    os.rename(filename, (new_image_name + ".jpg"))
                elif (filename.endswith(".cr2")):
                    os.rename(filename, (new_image_name + ".cr2"))

    def _blur_detection(self, image_path):
        """."""
        # This function evaluates wether a image is burry or not
        black_pixel = 0
        white_pixel = 0
        src_image = cv2.imread(image_path + ".jpg")
        median_image = cv2.medianBlur(src_image, 5)
        gray_image = cv2.cvtColor(median_image, cv2.COLOR_RGB2GRAY)
        adaptive_image = cv2.adaptiveThreshold(gray_image, 255,
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 11, 2)
        resized_image = cv2.resize(adaptive_image, (0, 0), fx=0.15, fy=0.15)
        # Goes to thourgh each pixel position
        for i in range(resized_image.shape[0]):
            for j in range(resized_image.shape[1]):
                # Evaluates the pixels' value
                if (resized_image[i, j] < 1):
                    black_pixel = black_pixel + 1
                elif (resized_image[i, j] > 254):
                    white_pixel = white_pixel + 1
        pixel_ratio = black_pixel / white_pixel * 1000
        if (pixel_ratio > 10):
            self.log.log("_blur_detection() not blurred " + str(pixel_ratio),
                         level=3, days_to_remain=1)
            return ("Not Blurry")
        else:
            self.log.log("_blur_detection() blurred " + str(pixel_ratio),
                         level=3, days_to_remain=1)
            return ("Blurry")

    def _delete_image(self, image_path):
        """."""
        # This function deletes an image depending on the ID given
        os.remove(image_path + ".jpg")
        os.remove(image_path + ".cr2")
