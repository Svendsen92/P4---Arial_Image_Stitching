from Image_manager import image_manager

savePath = "/home/pi/Desktop/"
imageId = "test"
iteration = 0

state = image_manager.aquirePicture(imageId, savePath, iteration)

if (state == True):
    print ("aquired image")
else:
    print ("Image not aquired")
