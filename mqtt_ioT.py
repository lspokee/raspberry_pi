import time
import Adafruit_DHT
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def on_message(client, userdata, message):
    if("aircon" in message.topic):
        print("air")
        if("ON" in str(message.payload.decode("utf-8"))):
            GPIO.output(FAN_PIN, False)
        else:
            GPIO.output(FAN_PIN, True)
    if("light" in message.topic):
        print("light")
        if("ON" in str(message.payload.decode("utf-8"))):
            GPIO.output(LIGHT_PIN, False)
        else:
            GPIO.output(LIGHT_PIN, True)


SENSOR = 23
FAN_PIN = 17
LIGHT_PIN = 27

GPIO.setup(SENSOR,GPIO.IN)
GPIO.setup(FAN_PIN,GPIO.OUT)
GPIO.setup(LIGHT_PIN,GPIO.OUT)


client=mqtt.Client()
client.username_pw_set("iehgauaw","r1a4Z3i0rMwH")
client.connect("tailor.cloudmqtt.com",15323,60)
client.on_message = on_message
client.subscribe("aircon")
client.subscribe("light")

GPIO.output(FAN_PIN, True)
GPIO.output(LIGHT_PIN, True)



while True:
    h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, SENSOR)
    client.publish("temp",int(t))
    client.publish("humid",int(h))
    client.loop_start()
    time.sleep(1)


