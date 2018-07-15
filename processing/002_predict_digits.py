from scipy.misc import imread, imresize
import numpy as np
from keras.models import load_model
import pandas as pd

# model_path = '/home/hkromer/Documents/02_solaranlage/MNIST_trained/cnn.h5'
model_path = '/home/hkromer/Documents/02_solaranlage/MNIST_trained/mnist-neural.h5'

model = load_model(model_path)

def predict_digits(img):
	# img = '/home/hkromer/Documents/02_solaranlage/2018-07-14_17-02/image8_04_digit_6_filtered.png'
	x = imread(img,mode='L')
	#compute a bit-wise inversion so black becomes white and vice versa
	x = np.invert(x)
	#make it the right size
	x = imresize(x,(28,28))
	#convert to a 4D tensor to feed into our model
	# x = x.reshape(1,28,28,1)
	x = x.reshape(1,784)
	x = x.astype('float32')
	x /= 255

	#perform the prediction

	
	out = model.predict(x)

	# print(out)
	# print(np.argmax(out))
	this_digit = np.argmax(out)

	return this_digit

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


	df = predict_all_digits(lst_directories[kk])

	df.to_csv('df_digits2.csv')
		
	