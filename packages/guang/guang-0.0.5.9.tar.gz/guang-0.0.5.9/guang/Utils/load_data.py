
def load_mnist(SIZE=128):
	'''
	SIZE: points image size
	'''
	import numpy as np 
	import cv2
	from tensorflow.keras.datasets import mnist
	(x_train, _), (x_test, _) = mnist.load_data()
	x_train = x_train.astype('float32') / 255.
	x_test = x_test.astype('float32') / 255.
	x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  
	x_test = np.reshape(x_test, (len(x_test), 28, 28, 1)) 

	x_train = x_train[:2000]
	x_test = x_test[:1000]

	X_train, X_test = x_train[0][...,-1], x_test[0][...,-1]

	X_train, X_test = cv2.resize(X_train, (SIZE,SIZE)), cv2.resize(X_test, (SIZE,SIZE))
	X_train, X_test = X_train.reshape(1,SIZE,SIZE,1), X_test.reshape(1,SIZE,SIZE,1)
	for i, j in zip(x_train, x_test):
		x_i = cv2.resize(i[...,-1], (SIZE, SIZE))
		x_j = cv2.resize(j[...,-1], (SIZE, SIZE))
		X_train = np.concatenate((X_train, x_i.reshape(1,SIZE,SIZE,1)), axis=0)
		X_test = np.concatenate((X_test, x_j.reshape(1,SIZE,SIZE,1)), axis=0)
	
	return X_train, X_test