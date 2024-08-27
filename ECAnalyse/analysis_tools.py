import numpy as np

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


def x_intercept(m, c):
	# y =  mx+c, 0 = mx+c, x = -c/m
	return -c / m


def radians_to_degrees(angle):
	return (angle / (2*np.pi)) * 360


def slice_indices(x, n):
	length = len(x)
	indices = np.array(list(range(n)))
	iteration = np.array([1] * n)
	indices_list = [indices]
	while indices[-1] < length - 1:
		indices = np.add(indices, iteration)
		indices_list.append(indices)
	return indices_list


def lorentzian(x, I, x0, w):
	# Returns a lorentzian function for the supplied x values
	# I is intensity, x0 is centre of function and w is width
	# at half height
	return I * (w/2) ** 2/ ((x-x0)**2 + (w/2)**2)


def differentiated_lorentzian(x, I, x0, w):
	denom_term = (x-x0)**2 + (w/2)**2
	term1 = I*(w/2)**2 / denom_term**2
	term2 = 2*(x-x0)
	return -term2 * term1


def gaussian(x, I, x0, stdev):
	# Returns a Gaussian function for the supplied x values
	# I is intensity, x0 is the centre of functiond and stdev is 
	# the standard deviation
	return I * np.exp(-(x-x0)**2 / (2*stdev**2))




