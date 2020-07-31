import numpy as np
import cv2
import os
from CarBrain import CarBrain

#lowerBound = np.array([33,80,40])
#upperBound = np.array([102,255,255])

#White
lowerBound = np.array([0,0,240], dtype=np.uint8)
upperBound = np.array([255,15,255], dtype=np.uint8)

kernalOpen = np.ones((5,5))
kernalClose = np.ones((20,20))
imgs_list=[]

carBrain = CarBrain()

# Load an color image in grayscale
pth = "data"
print(pth)
for (dirpath, dirnames, filenames) in os.walk(pth):
    if len(filenames) != 0:
        dirnames = dirpath.split("\\")
        dirname = dirnames[len(dirnames)-1]
        print(dirname)
        for filename in filenames:
            print(dirpath+"\\"+filename)
            im = cv2.imread(dirpath+"/"+filename)
            img = cv2.resize(im, (320,240))
            imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(imgHSV, lowerBound, upperBound)
            image_array = np.zeros([1,240,320])
            image_array[0] = mask
            direction = carBrain.get_direction(image_array)
            print(direction)
            font = cv2.FONT_HERSHEY_SIMPLEX
            if len(direction) > 0:
                cv2.putText(mask,direction[0],(120,180), font, 0.5,(255,255,255),2,cv2.LINE_AA)
            print("writing to "+'car/steerpredict/'+dirname+'/'+filename)
            outDir = 'steerpredict/'+dirname
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            cv2.imwrite(outDir+'/'+filename, mask)