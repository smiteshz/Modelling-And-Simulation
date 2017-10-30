import numpy as np

def integral_evaluation(N):
	x_samples = np.random.uniform(0,1,N)
	y_samples = np.random.uniform(0,np.pi/2,N)
	z_samples = np.random.uniform(0,1,N)
	z_samples_test=np.sum(function_cos_sin(x_samples,y_samples)>z_samples)
	avg = (z_samples_test/N)*(np.pi/2)
	print(avg)
	return()

def function_cos_sin(x,y):
	return(np.exp(np.cos(x+y)))

def function_single(x):
	return(np.cos(x)*np.exp(np.sin(x)))

integral_evaluation(1000)