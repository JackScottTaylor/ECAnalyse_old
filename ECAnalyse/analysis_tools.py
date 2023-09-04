import numpy as np
import scipy

def moving_average(a, n=3):
	# Returns the moving average over n points for the provided
	# array, a and returns a numpy array
	# Taken from 'https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-python-numpy-scipy
	ret = np.cumsum(a, dtype=float)
	ret[n:] = ret[n:] - ret[:-n]
	return ret[n - 1:] / n


def integrate(x, y):
	# x and y should be numpy arrays of the same size ideally. The function should return
	# a numpy array of ∫ydx from the start of the x array using the trapezium rule
	ydx = np.zeros(len(x))
	cumulative = 0
	for i in range(1, len(x)):
		a, b, dx = y[i-1], y[i], x[i] - x[i-1]
		cumulative += 0.5 * (a + b) * dx
		ydx[i] = cumulative
	return ydx


def differentiate(x, y):
	# Uses the numpy gradient function which returns an array the same length as the
	# ones provided via x and y
	return np.gradient(y, x)


def line_of_best_fit(x, y):
	# Takes two numpy arrays, x and y. Performs linear regression to find
	# the line of best fit for the data and returns two floats m and c,
	# which correspond to y=mx+c
	m, c = np.polyfit(x, y, 1)
	return m, c


def standard_deviation(y, y_model):
	# Takes two narrays y and y_model. y is the actual data set and y_model
	# is the modelled data set (may be the moving average or similar). The
	# residual standard deviation of the data set is then calculated against
	# the model data
	residuals = np.subtract(y, y_model) ** 2
	numerator = np.sum(residuals)
	denominator = len(y)
	sigma = np.sqrt(numerator / denominator)
	return sigma


def standard_deviation_of_mean(y, y_model):
	return standard_deviation(y, y_model) / np.sqrt(len(y))




