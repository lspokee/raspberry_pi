#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER_LEFT = 26
GPIO_ECHO_LEFT = 20
GPIO_TRIGGER_RIGHT = 22
GPIO_ECHO_RIGHT = 23
GPIO_OUTPUT_PIN_LEFT = 21
GPIO_OUTPUT_PIN_RIGHT = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
GPIO.setup(GPIO_OUTPUT_PIN_LEFT, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)
GPIO.setup(GPIO_OUTPUT_PIN_RIGHT, GPIO.OUT)

 
def distance(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
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
        print("START")
        while True:
            dist_left = distance(GPIO_TRIGGER_LEFT,GPIO_ECHO_LEFT)
            if int(dist_left)-120 >0:
                GPIO.output(GPIO_OUTPUT_PIN_LEFT, GPIO.LOW)        
            else:
                GPIO.output(GPIO_OUTPUT_PIN_LEFT, GPIO.HIGH)
                
            dist_right = distance(GPIO_TRIGGER_RIGHT,GPIO_ECHO_RIGHT)            
            if int(dist_right)-120 >0:
                GPIO.output(GPIO_OUTPUT_PIN_RIGHT, GPIO.LOW)
                #time.sleep(5)
            else:
                GPIO.output(GPIO_OUTPUT_PIN_RIGHT, GPIO.HIGH)
            print ("Measured Distance: LEFT = %.1f cm RIGHT = %.1f cm" % (dist_left,dist_right))
            time.sleep(0.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

