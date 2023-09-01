import numpy as np

def moving_average(a, n=3):
	# Returns the moving average over n points for the provided
	# array, a and returns a numpy array
	# Taken from 'https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-python-numpy-scipy
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n

