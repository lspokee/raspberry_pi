import RPi.GPIO as GPIO
import time
 
GPIO_PIR_INPUT_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIR_INPUT_PIN, GPIO.IN)
GPIO_OUTPUT_PIN = 5
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT) 
try:
    while True:
        signal = GPIO.input(GPIO_PIR_INPUT_PIN)
        if signal>0:
            GPIO.output(GPIO_OUTPUT_PIN, GPIO.HIGH)
            #time.sleep(5)
        else:
            GPIO.output(GPIO_OUTPUT_PIN, GPIO.LOW)
except KeyboardInterrupt:
    print('interrupted')
finally:
    GPIO.cleanup()
