#from pynput import keyboard
import RPi.GPIO as GPIO
import time
import cv2

PINS = {'FORWARD':32, 'BACKWARD':35, 'LEFT':31, 'RIGHT':33}

class Car:    
    def __init__(self):
        print('Initializing pins')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(32,GPIO.OUT)
        GPIO.setup(31,GPIO.OUT)
        GPIO.setup(35,GPIO.OUT)
        GPIO.setup(33,GPIO.OUT)
        GPIO.output(32,GPIO.HIGH)
        GPIO.output(31,GPIO.HIGH)
        GPIO.output(33,GPIO.HIGH)
        GPIO.output(35,GPIO.HIGH)
        print('Initializing pins finished')
    
    def move(self, direction):
        print('Moving ', direction)
        for dir in direction :
            GPIO.output(PINS[dir], GPIO.LOW)
            if dir == 'RIGHT' or dir == 'LEFT':
                time.sleep(0.2)
        time.sleep(0.4)
        self.stop(direction)
            
    def stop(self, direction):
        print('Stopping ', direction)
        for dir in direction :
            GPIO.output(PINS[dir], GPIO.HIGH)
        time.sleep(1)
        
    def destroy(self):
        print('Cleaning up')
        GPIO.cleanup()
