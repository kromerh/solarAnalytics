from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps    
import os, glob
import re
import numpy as np
import sys
import pandas as pd

from scipy.misc import imread, imresize
import numpy as np

# path to the images. in each subfolder there is a new timestamp
path_raw_images = '/media/data/solarAnlage/raw_images/'

# path to the cropped digits
path_cropped_digits = '/media/data/solarAnlage/image_processing/'

# loop through the subfolders and crop around each digit
subfolders = [f for f in os.listdir(path_raw_images)]
paths = ["{}/{}/".format(path_raw_images,f) for f in subfolders]

# loop through the images
# crop the image around the region of interest
# returns one image rotated and cropped
def rotate_and_crop_image(img_path):
	# open the image
	img = Image.open(img_path)
	date = re.findall(r'(\d\d\d\d-\d\d-\d\d_\d\d-\d\d)',img_path)[0]
	imgNr = re.findall(r'(image\d).jpg',img_path)[0]

	# rotate
	img = img.rotate(272-180, resample=Image.BICUBIC, expand=True)  # rotate image

	# crop
	# box = (815, 1345, 920, 1380)
	box = (815-100, 1345-100, 920+100, 1380+100)
	img = img.crop(box)

	# save rotated and cropped
	saveDir = "{}/{}/cropped/".format(path_cropped_digits,date)
	if not os.path.exists(saveDir):
		os.makedirs(saveDir)
	save_path_img_rotated = '{}/{}.png'.format(saveDir,imgNr)
	img.save(save_path_img_rotated)
	sys.exit()


# image numbers are from 0 to 9
imgs = ["image{}.jpg".format(ii) for ii in range(0,10)]

# loop through the subfolder paths
ii = 0
for path in paths:
	print("Doing path {} out of {}".format(ii, len(paths)))
	# loop through the images
	for this_img in imgs:
		this_path = "{}/{}".format(path, this_img)
		rotate_and_crop_image(this_path)
		# sys.exit()
	# sys.exit()
	ii = ii + 1