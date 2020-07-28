import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from CarBrain import CarBrain
from Car import Car

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])
carBrain = CarBrain()
car = Car()

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
print('hey') 
# allow the camera to warmup
time.sleep(0.1)

try :
 
# capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        im = frame.array
        cv2.resize(im,(320,240))
        img = cv2.resize(im, (320,240))
        #cv2.imshow('IP Camera stream',img)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, lowerBound, upperBound)
        #cv2.imshow('mask',mask)
        image_array = np.zeros([1,240,320])
        image_array[0] = mask
        direction = carBrain.get_direction(image_array)
        #print(direction)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(mask,direction[0],(120,180), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        #cv2.imshow('mask with direction',mask)
        car.move(direction)
        rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            car.destroy()
            break
finally:
    print('closing')
    car.destroy()

cv2.destroyAllWindows()
