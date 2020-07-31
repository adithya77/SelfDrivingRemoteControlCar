from pynput import keyboard
import RPi.GPIO as GPIO
import time
import cv2

def on_press(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc: return False # stop listener
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32,GPIO.OUT)
    GPIO.setup(31,GPIO.OUT)
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(33,GPIO.OUT)
    GPIO.output(32,GPIO.HIGH)
    GPIO.output(31,GPIO.HIGH)
    GPIO.output(33,GPIO.HIGH)
    GPIO.output(35,GPIO.HIGH)
    
    if k in ['up']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key pressed: ' + k, ' going straight')
        #GPIO.output(36,GPIO.HIGH)
        GPIO.output(32,GPIO.LOW)
    if k in ['down']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key pressed: ' + k, ' going back')
        #GPIO.output(32,GPIO.HIGH)
        GPIO.output(33,GPIO.LOW)
    if k in ['left']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key pressed: ' + k, ' going left')
        #GPIO.output(35,GPIO.HIGH)
        GPIO.output(31,GPIO.LOW)
    if k in ['right']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key pressed: ' + k, ' going right')
        #GPIO.output(37,GPIO.HIGH)
        GPIO.output(35,GPIO.LOW)
    if k == 'q':
        print('cleaning')
        GPIO.cleanup()
        
def on_release(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc: return False # stop listener
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(37,GPIO.OUT)
    
    if k in ['up']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key release: ' + k, ' stop going straight')
        GPIO.output(32,GPIO.HIGH)
    if k in ['down']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key release: ' + k, ' stop going back')
        GPIO.output(33,GPIO.HIGH)
    if k in ['left']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key release: ' + k, ' stop going left')
        GPIO.output(31,GPIO.HIGH)
    if k in ['right']: # keys interested
        # self.keys.append(k) # store it in global-like variable
        print('Key release: ' + k, ' stop going right')
        GPIO.output(35,GPIO.HIGH)      
        #return False # remove this if want more keys

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(32,GPIO.OUT)
#GPIO.output(32,GPIO.LOW)
#time.sleep(3)
#GPIO.output(32,GPIO.HIGH)


lis = keyboard.Listener(on_press=on_press, on_release=on_release)
lis.start() # start to listen on a separate thread
lis.join() 