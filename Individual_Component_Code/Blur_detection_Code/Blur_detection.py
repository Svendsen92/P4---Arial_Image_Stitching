import cv2

imagePath = "/home/pi/Desktop/Test_Img_Folder/img"
 
for k in range (1,9):

    blackPixel = 0
    whitePixel = 0
    
    src_image = cv2.imread(imagePath + str(k) + ".JPG")
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
                
            if (resized_image[i,j] > 254):
                whitePixel = whitePixel +1

    pixelRatio = blackPixel / whitePixel * 1000

    if (pixelRatio > 19):
        text = "Not Blurry"
    else:
        text = "Blurry"
    
    print ("\n" + "Image" + str(k) + "\n")
    print ("blackPixel = " + str(blackPixel) + "\n")
    print ("whitePixel = " + str(whitePixel) + "\n")
    print ("pixelRatio = " + str(pixelRatio) + "\n")
    print (text + "\n")
    
    # show the image
    cv2.imshow("Image" + str(k), resized_image)
    
key = cv2.waitKey(0)
