#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 26
GPIO_ECHO = 20
GPIO_PIR_INPUT_PIN = 24
GPIO_OUTPUT_PIN = 5
GPIO_FILM_PIN = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_PIR_INPUT_PIN, GPIO.IN)
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT)
GPIO.setup(GPIO_FILM_PIN, GPIO.OUT)

 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    #print ("Measured Distance = %.1f cm" % distance)
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if int(dist)-120 >0:
                GPIO.output(GPIO_FILM_PIN, GPIO.LOW)        
            else:
                GPIO.output(GPIO_FILM_PIN, GPIO.HIGH)            
            signal = GPIO.input(GPIO_PIR_INPUT_PIN)
            if signal>0:
                GPIO.output(GPIO_OUTPUT_PIN, GPIO.HIGH)
                #time.sleep(5)
            else:
                GPIO.output(GPIO_OUTPUT_PIN, GPIO.LOW)
            time.sleep(0.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
