import cv2
import numpy as np
from CarBrain import CarBrain

stream = cv2.VideoCapture('http://192.168.0.100:8080/video')

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')  

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])
carBrain = CarBrain()

while True:

    r, im = stream.read()
    cv2.resize(im,(320,240))
    img = cv2.resize(im, (320,240))
    cv2.imshow('IP Camera stream',img)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    cv2.imshow('mask',mask)
    image_array = np.zeros([1,240,320])
    image_array[0] = mask
    direction = carBrain.get_direction(image_array)
    #print(direction)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(mask,direction[0],(120,180), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('mask with direction',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()