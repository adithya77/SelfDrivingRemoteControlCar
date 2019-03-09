import CarBrain
import cv2
import numpy as np

stream = cv2.VideoCapture('http://192.168.0.107:8080/video')

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')  
lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])
carBrain = CarBrain.CarBrain()

while True:

    r, f = stream.read()
    cv2.resize(f,(340,220))
    img = cv2.resize(f, (340,220))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    #direction = carBrain.get_direction(mask)

    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(f,direction,(10,10), font, 4,(255,255,255),2,cv2.LINE_AA)
    #cv2.imshow('IP Camera stream',f)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
