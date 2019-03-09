import cv2
import numpy
import os


basePath = "D:/adi/prj/car/data"
right = basePath+"/RIGHT"
left = basePath+"/LEFT"
for (dirpath, dirnames, filenames) in os.walk(right):
    if len(filenames) != 0:
        for filename in filenames:
            print(dirpath+"\\"+filename)
            im = cv2.imread(dirpath+"/"+filename)
            horizontal_img = cv2.flip(im, 1)
            cv2.imwrite(left+'/'+filename, horizontal_img)