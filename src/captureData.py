import sys
import termios
import contextlib
import random
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import RPi.GPIO as GPIO
from Car import Car
import os

lowerBound = np.array([33,80,40])
upperBound = np.array([102,255,255])

car = Car()

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def main():
    print('exit with ^C or ^D')
    pressed = False
    with raw_mode(sys.stdin):
        try:
            while True:
                #print('hey')
                ch = sys.stdin.read(1)
                #print('heyo')
                #print(ch)
                if not ch or ch == chr(4):
                    if pressed == True:
                        print('Released')
                        pressed = False
                    #break
                    continue
                #print('%02x' % ord(ch),)
                pressed = True
                nums = ord(ch)
                #print('hello')
                #print(nums)
                if nums == 65:
                    print('up')
                    on_press(['FORWARD'])
                elif nums == 66:
                    print('down')
                    on_press(['BACKWARD'])
                elif nums == 67:
                    print('right')
                    on_press(['RIGHT','FORWARD'])
                elif nums == 68:
                    print('left')
                    on_press(['LEFT','FORWARD'])
        except (KeyboardInterrupt, EOFError):
            print('cleaning')
            GPIO.cleanup()
            pass

def on_press(key):
    print('inside on_press ', key)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    outDir = '/home/pi/car/data/'+key[0]
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    #print(frame.shape)
    path = outDir+'/'+str(random.randint(1,10000))+'.jpg'
    print(path)
    cv2.imwrite(path, mask)
    rawCapture.truncate(0)
    car.move(key)

if __name__ == '__main__':
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 240))
    main()