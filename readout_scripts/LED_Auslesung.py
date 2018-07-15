from PIL import Image, ImageEnhance, ImageFilter
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import datetime 
import os
import sys

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Get current time
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d_%H-%M")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# path
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
path = '/home/pi/Documents/'

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Make folder
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
os.system('mkdir %s/%s' %(path, date))
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# START LED
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
print("LED on")
GPIO.output(18,GPIO.HIGH)
time.sleep(5)
print("LED off")
GPIO.output(18,GPIO.LOW)