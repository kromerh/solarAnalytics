# Eingehend: 1.8.0: ca 2300 kWh -> wird vom Netz gekauft a la 30 c
# Ausgehend: 2.8.0: ca 1100 kWh -> wird ins Netz eingespeist a la 11 c

from PIL import Image, ImageEnhance, ImageFilter
import PIL.ImageOps    
import os, glob
import re
import numpy as np
import sys
import pandas as pd

from scipy.misc import imread, imresize
import numpy as np
from keras.models import load_model


def predict_digits(img):
	# img = '/home/hkromer/Documents/02_solaranlage/2018-07-14_17-02/image8_04_digit_6_filtered.png'
	x = imread(img,mode='L')
	#compute a bit-wise inversion so black becomes white and vice versa
	x = np.invert(x)
	#make it the right size
	x = imresize(x,(28,28))
	#convert to a 4D tensor to feed into our model
	x = x.reshape(1,28,28,1)
	x = x.astype('float32')
	x /= 255

	#perform the prediction

	model_path = '/home/hkromer/Documents/02_solaranlage/MNIST_trained/cnn.h5'
	model = load_model(model_path)
	out = model.predict(x)

	# print(out)
	# print(np.argmax(out))
	this_digit = np.argmax(out)

	return this_digit



# returns one image rotated and cropped
def rotate_and_crop_image(img, img_path):

	# rotate
	img = img.rotate(272-180, resample=Image.BICUBIC, expand=True)  # rotate image

	# crop
	box = (829, 1391, 1034, 1431)
	img = img.crop(box)

	# save rotated and cropped
	_ = re.findall(r'(.+).jpg', img_path)
	save_path_img_rotated = '{}_01_rotated.png'.format(_[0])
	img.save(save_path_img_rotated)

	return img



# returns a list with the image of each digit
# crop around each digit
def crop_around_each_digit(img, img_path):
	_ = re.findall(r'(.+).jpg', img_path)
	save_path_img = _[0]

	# crop digit 1
	px1 = [41, 58]
	py = [0, 33]
	# crop digit 2
	px2 = [58, 75]
	# crop digit 3
	px3 = [75, 92] # +17
	# crop digit 4
	px4 = [92, 109]
	# crop digit 5
	px5 = [109, 126]
	# crop digit 6
	px6 = [126, 143]

	lst_px = [px1, px2, px3, px4, px5, px6]

	lst_digits = []  # images of each digit
	for ii in range(0,len(lst_px)):
		px = lst_px[ii]
		# crop
		box = (px[0], py[0], px[1], py[1])
		this_img = img.crop(box)
		# if ii == 4:
		# 	# for the last digit: remove the stuff in the corner
		# 	lst_x = np.arange(px5_remove[0],px5_remove[1],1)
		# 	lst_y = np.arange(py5_remove[0],py5_remove[1],1)
		# 	pixels = this_img.load()
		# 	for x in lst_x:
		# 		for y in lst_y:
		# 			x = int(x)
		# 			y = int(y)
		# 			pixels[x, y] = (255, 255, 255)

		
		this_img.save('{}_03_digit_{:.0f}.png'.format(save_path_img,ii+1))
		lst_digits.append(this_img)
		ii = ii + 1

	return lst_digits

# returns nothing, filters the images and saves it
def filter_image(lst_digits, img_path):
	ii = 0
	for img in lst_digits:
		# filtering
		_ = re.findall(r'(.+).jpg', img_path)
		save_path_img = _[0]


		# rescale the image
		basewidth = 300
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		# erosion and blur filter
		img = img.filter(ImageFilter.MinFilter(3))
		img = img.filter(ImageFilter.GaussianBlur(3))

		# mask to filter the numbers
		img = img.convert("L")
		th = 155 # the value has to be adjusted for an image of interest 
		img = img.point(lambda i: i < th and 255)		
		img = PIL.ImageOps.invert(img)  # invert image
		img.save('{}_04_digit_{:.0f}_filtered.png'.format(save_path_img,ii+1))

		ii = ii + 1


def predict_all_digits(path):
	idx = np.arange(0,10,1)  # all the images
	digits = np.arange(1,7,1)  # all the digits
	df = pd.DataFrame()
	for ii in idx:
		s_digit = []
		for digit in digits:
			# image with the digits
			this_img = '{}image{:.0f}_04_digit_{:.0f}_filtered.png'.format(path,ii,digit)
			s = predict_digits(this_img)
			s_digit.append(s)
		df['image{:.0f}'.format(ii)] = s_digit

	return df
	
	# predict_digits(img)


# path to the images
# path = "/home/hkromer/Documents/02_solaranlage/2018-07-14_16-44/"
path = "/home/hkromer/Documents/02_solaranlage/2018-07-14_17-02/"


lst_directories = [path]  # list of all the directories


for kk in range(0,len(lst_directories)):
	print('Processing directory: {}'.format(lst_directories[kk]))
	lst_img = ['{}image{}.jpg'.format(path,it) for it in [0,1,2,3,4,5,6,7,8,9]]
	
	for img_path in lst_img:
		img = Image.open(img_path)

		img = rotate_and_crop_image(img, img_path)
		# sys.exit()

		lst_digits = crop_around_each_digit(img, img_path)

		filter_image(lst_digits, img_path)

	df = predict_all_digits(lst_directories[kk])
		
	df.to_csv('df.csv')
