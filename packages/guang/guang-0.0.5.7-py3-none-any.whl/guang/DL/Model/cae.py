# tensorflow2.0
import tensorflow as tf
from tensorflow.keras import Input,Model
from tensorflow.keras.layers import Conv2D,MaxPooling2D, UpSampling2D


class CAE:
	def __init__(self,w, h, input_channel):
	 self.w, self.h, self.input_channel = w, h, input_channel

	def compile(self):
		input_img = Input(shape=(self.w,self.h,self.input_channel))
		x = Conv2D(16, (3, 3),strides=(2,2), activation='relu', padding='same')(input_img)
		x = Conv2D(8, (3, 3), strides=(2,2), activation='relu', padding='same')(x)
		encoded = Conv2D(8, (3, 3), strides=(2,2), activation='relu', padding='same')(x)

		x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
		t_b, t_h,t_w, t_c = x.shape
		x = tf.image.resize(x, ( t_w*2, t_h*2))
		x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
		t_b, t_h,t_w, t_c = x.shape
		x = tf.image.resize(x, ( t_w*2, t_h*2))
		x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
		t_b, t_h,t_w, t_c = x.shape
		x = tf.image.resize(x, ( t_w*2, t_h*2))
		decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

		self.autoencoder = Model(input_img, decoded)
		self.autoencoder.compile(optimizer='adam', loss='binary_crossentropy') 
	
	def fit(self,x_train, x_test):

		self.autoencoder.fit(x_train, x_train,
						epochs=5,
						batch_size=128,
						shuffle=True,
						validation_data=(x_test, x_test)
					)


def TEST(SIZE=128):
	'''
	SIZE: Specify image size
	'''
	from tensorflow.keras.datasets import mnist
	import numpy as np
	import matplotlib.pyplot as plt
	(x_train, _), (x_test, _) = mnist.load_data()

	x_train = x_train.astype('float32') / 255.
	x_test = x_test.astype('float32') / 255.
	x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  # adapt this if using `channels_first` image data format
	x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))  # adapt this if using `channels_first` image data format

	x_train = x_train[:10000]
	x_test = x_test[:1000]
	import cv2
	X_train, X_test = x_train[0][...,-1], x_test[0][...,-1]
	X_train, X_test = cv2.resize(X_train, (SIZE,SIZE)), cv2.resize(X_test, (SIZE,SIZE))
	X_train, X_test = X_train.reshape(1,SIZE,SIZE,1), X_test.reshape(1,SIZE,SIZE,1)
	for i, j in zip(x_train, x_test):
		x_i = cv2.resize(i[...,-1], (SIZE, SIZE))
		x_j = cv2.resize(j[...,-1], (SIZE, SIZE))
		X_train = np.concatenate((X_train, x_i.reshape(1,SIZE,SIZE,1)), axis=0)
		X_test = np.concatenate((X_test, x_j.reshape(1,SIZE,SIZE,1)), axis=0)
		
	x_train, x_test = X_train, X_test
	w, h, input_channel = 28, 28, 1
	cae = CAE(w, h, input_channel)
	cae.compile()
	cae.fit(x_train, x_test)

	decoded_imgs = cae.autoencoder.predict(x_test[:20])

	n = 5                                        
	plt.figure(figsize=(10, 4))
	for i in range(1,n+1):
		# display original
		ax = plt.subplot(2, n, i)
		plt.imshow(x_test[i].reshape(w,h))
		plt.gray()
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)

		# display reconstruction
		ax = plt.subplot(2, n,i+n)
		plt.imshow(decoded_imgs[i].reshape(w,h))
		plt.gray()
		ax.get_xaxis().set_visible(False)
		ax.get_yaxis().set_visible(False)
	plt.show()
if __name__=='__main__':
	TEST()