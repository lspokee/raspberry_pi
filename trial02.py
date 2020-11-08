import RPi.GPIO as GPIO
import time
 
GPIO_PIR_INPUT_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR_INPUT_PIN, GPIO.IN)
try:
    while True:
        signal = GPIO.input(GPIO_PIR_INPUT_PIN)
        #print('signal')
        print(signal)
        #time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()
