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
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
print("LED on")
GPIO.output(17,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
time.sleep(5)
