#import library part#
import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

#pin mode & cleanup IO pin
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


#pin set up part#
DHT11 = 23 #dh11 data pin
TRIG = 17 #ultrasonic
ECHO = 27 #ultrasonic
CONTROL_PIN = 22 #servo motor
LDR_PIN = 24 #LDR sensor
LIGHT_PIN = 25 #LDR LED pin
FLAME_PIN = 21 #flame sensor pin
BUZZER_PIN = 20 #buzzer pin
BUTTON_PIN = 16 #button pin

#io setup
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(DHT11,GPIO.IN)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(FLAME_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN,GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)

#variable/method declare
pwm_buzz = GPIO.PWM(BUZZER_PIN, 5000)
GPIO.output(BUZZER_PIN, True)
ldr_threshold = 600
PWM_FREQ = 50
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

#MQTT declare
client=mqtt.Client()
client.username_pw_set("iehgauaw","yR981mnloMkT")#replace with your user name and password
client.connect("tailor.cloudmqtt.com",15323,60)

#servo motor method
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

#LDR method
def readLDR():
    reading = 0
    GPIO.setup(LDR_PIN, GPIO.OUT)
    GPIO.output(LDR_PIN, False)
    time.sleep(0.1)
    GPIO.setup(LDR_PIN, GPIO.IN)
    while (GPIO.input (LDR_PIN) == False):
        reading=reading+1
    return reading

#Flame sensor method
def flame_call_back(FLAME_PIN):
    #start buzzing
    pwm_buzz.start(80)
    print("fire detected")
    client.publish("sensor/flame",1)

#Flame detected interrupt event handler (if detected fire, call flame sensor method)
GPIO.add_event_detect(FLAME_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(FLAME_PIN, flame_call_back)

#Button callback method
def button_call_back(BUTTON_PIN):
    #stop buzzing
    pwm_buzz.stop()
    client.publish("sensor/flame",0)

#Button interrupt to stop buzzing
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=300)
GPIO.add_event_callback(BUTTON_PIN, button_call_back)

#infinity loop
while True:
    
    #ultrasonic part
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
    
    #servo motor part (if distance shorter than 15cm auto open door)
    if distance < 15:
        print("<15cm detected")
        #open
        dc = angle_to_duty_cycle(90) #0 degree
        pwm.ChangeDutyCycle(dc)
        time.sleep (3)
        #close
        dc = angle_to_duty_cycle(0)#90 degree
        pwm.ChangeDutyCycle(dc)
        time.sleep (3)
    
    
    #dht11 part
    h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11)
    if h is not None and t is not None:
        print('Temp={0:0.1f}C Humid={1:0.1f}%'.format(t, h))
    else:
        print('DHT11 failed')
    
    #LDR part
    ldr_reading = readLDR()
    if ldr_reading < ldr_threshold:
        GPIO.output(LIGHT_PIN, False)
        client.publish("sensor/light",0)
    else:
        GPIO.output(LIGHT_PIN, True)
        print("light turned on")
        client.publish("sensor/light",1)
        
    
    #cloud mqtt part
    client=mqtt.Client()
    client.username_pw_set("iehgauaw","yR981mnloMkT")#replace with your user name and password
    client.connect("tailor.cloudmqtt.com",15323,60)
    client.publish("sensor/temp",int(t))
    client.publish("sensor/humid",int(h))
    print("MQTT sent")