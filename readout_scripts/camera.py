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

# # Start IR 
# GPIO.setup(17,GPIO.OUT)
# GPIO.setup(27,GPIO.OUT)
# print("IR on")
# GPIO.output(17,GPIO.LOW)
# GPIO.output(27,GPIO.LOW)
# time.sleep(5)
# sys.exit()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Wait 10 seconds
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("Sleeping for 10 seconds")
time.sleep(10)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Take 10 images with 5 second sleep
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("Taking 10 images with 5 second sleep")
camera = PiCamera()
camera.resolution = (2592,1944)
camera.framerate = 15
camera.start_preview()
for ii in range(0,10):
	sleep(5)
	camera.capture('/home/pi/Documents/%s/image%s.jpg' % (date, ii))
	print("Saved image%s.jpg" % ii)
camera.stop_preview()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Crop images
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# dY=[1100, 1450]
# dX=[900, 1000]
# for ii in range(0,10):
# 	fname = '/home/pi/Documents/%s/image%s.jpg' % (date, ii)
# 	img = Image.open(fname)
# 	img = img.crop((dY[0], dX[0], dY[1], dX[1]))
# 	img.save(fname)
# Stop IR 
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
print("IR off")
GPIO.output(17,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
time.sleep(5)
