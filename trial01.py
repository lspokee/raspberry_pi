import RPi.GPIO as GPIO
import time
 
GPIO_PIN = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)
 
try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        print('LED 亮')
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        time.sleep(1)
        print('LED 熄')
        GPIO.output(GPIO_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()