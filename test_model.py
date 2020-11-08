import RPi.GPIO as GPIO
import time
import cv2
import tensorflow as tf
import io
import os
import picamera
from time import sleep
import numpy as np

#pin mode
GPIO.setmode(GPIO.BCM)

#no scientific notation mode
np.set_printoptions(suppress=True)

#object categories
CATEGORIES = ["trash","bottle","can","paper"]

#pinout
TRIG = 23 
ECHO = 24
DETECTED = 25 #red led
YELLOW = 20
GREEN = 21

#setup
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DETECTED,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)

while True:
    
    #ultrasonic & led control
    GPIO.output(DETECTED, False)
    GPIO.output(YELLOW, False)
    GPIO.output(GREEN, False)
    GPIO.output(TRIG, False)
    time.sleep(1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print ("Distance:",distance,"cm")
    
    # if distance shorter than 15cm object detection start
    if distance < 15:
        print("detected object")
        GPIO.output(DETECTED, True)
        time.sleep(1)
        
        #camera part
        with picamera.PiCamera() as camera:
            camera.resolution = (2592,1944) #5MP
            camera.iso = 800 #max iso of pi cam
            camera.shutter_speed = 400000
            camera.awb_mode = 'auto'
            sleep(3) #camera warm up
            camera.capture("/home/pi/Desktop/newimage.jpg")

        print("Picture taken")
        
        #image reshape & resize part
        def prepare(filepath): 
            IMG_SIZE = 100
            img_array = cv2.imread(filepath)
            new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        
        #declare model
        model = tf.keras.models.load_model("/media/pi/4EB9-D4F7/object_detection/trash.model")
        
        #input & predict via model
        prediction = model.predict([prepare('/home/pi/Desktop/newimage.jpg')])
        
        
        #print(prediction)
        #print(CATEGORIES[np.argmax(prediction[0])])
        
        if np.argmax(prediction[0]) == 1 or np.argmax(prediction[0]) == 2 or np.argmax(prediction[0]) == 3:
            print("recycle")
            GPIO.output(GREEN, True)
            time.sleep(5)
        elif np.argmax(prediction[0]) == 0:
            print("non-recycle")
            GPIO.output(YELLOW, True)
            time.sleep(5)