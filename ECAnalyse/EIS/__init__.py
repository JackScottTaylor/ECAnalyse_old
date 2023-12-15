from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print("Ready to Analyse EIS!!")

class EIS(EC_Lab_Txt_File):
	def __init__(self, file_path):
		super().__init__(file_path)


	def Nyquist(self, ax=plt.gca(), **kwargs):
		self.plot('Re', 'Im', ax=ax, **kwargs)
		ax.set_xlabel(r'Z$_\mathrm{R}$ / $\Omega$')
		ax.set_ylabel(r'-Z$_\mathrm{i}$ / $\Omega$')


	def linear_section(self, section=0.9, plot=False, ax=plt.gca(), **kwargs):
		# section determines how much of first part to ignore. Preset to use
		# last 10% of data to generate linear section.
		start_index = int(((len(self.get_data('Re')) - 1) * section) // 1)
		x, y = self.get_data('Re')[start_index:], self.get_data('Im')[start_index:]
		m, c = line_of_best_fit(x, y)
		if plot:
			x1, x2 = ax.get_xlim()
			ax.plot([x1, x2], [m*x1+c, m*x2+c], **kwargs)
		return m, c
	

	def linear_section_region(self, start, end, plot=False, ax=plt.gca(), **kwargs):
		# Start and end are in terms of the x_axis
		xs, ys = self.get_data('Re'), self.get_data('Im')
		x_section, y_section = [], []
		for x, y in zip(xs, ys):
			if x <= start or x >= end: continue
			x_section.append(x)
			y_section.append(y)

		m, c = line_of_best_fit(x_section, y_section)
		if plot:
			x1, x2 = ax.get_xlim()
			ax.plot([x1, x2], [m*x1+c, m*x2+c], **kwargs)
		return m, c
	

	def lsr(self, start, end, plot=False, ax=plt.gca(), **kwargs):
		# linear_section_region is a bit of a mouthful so have added this
		# as a shorter way of calling the function.
		m, c = self.linear_section_region(start, end, plot=plot, ax=ax, **kwargs)
		return m, c


	def Bode_Z(self, ax=plt.gca(), **kwargs):
		x = np.log(self.get_data('freq/Hz'))
		Re, Im = self.get_data('Re'), self.get_data('Im')
		absolute_Z = np.sqrt(np.add(np.multiply(Re, Re), np.multiply(Im, Im)))
		ax.set_xlabel(r'ln($\omega$ / Hz)')
		ax.set_ylabel('|Z| / $\Omega$)')
		ax.plot(x, absolute_Z, **kwargs)


	def Bode_arg(self, ax=plt.gca(), **kwargs):
		x = np.log(self.get_data('freq/Hz'))
		Re, Im = self.get_data('Re'), self.get_data('Im')
		absolute_Z = np.sqrt(np.add(np.multiply(Re, Re), np.multiply(Im, Im)))
		arg_Z = np.arctan(np.divide(-Im, Re))
		print(arg_Z)
		arg_Z = radians_to_degrees(arg_Z)
		print(arg_Z)
		ax.set_xlabel(r'ln($\omega$ / Hz)')
		ax.set_ylabel('Arg(Z) / $\degree$')
		ax.plot(x, arg_Z, **kwargs)
		ax.set_ylim((-90.01, 90.01))
		ax.set_yticks((-90, -45, 0, 45, 90))


	def Bode(self, ax=plt.gca()):
		self.Bode_Z(ax=ax)
		overlay_ax = ax.twinx()
		self.Bode_arg(color='firebrick', ax=overlay_ax)
		overlay_ax.spines['right'].set_color('firebrick')
		overlay_ax.yaxis.label.set_color('firebrick')
		overlay_ax.tick_params(axis='y', colors='firebrick')


	def R_A(self):
		# The minimum real value of the impedance which should
		# also have zero imaginary contribution
		Z_Re = self.get_data('Re')
		print(Z_Re)
		return np.min(Z_Re)


	def R_B(self):
		# This is the value of Z_real where the semi-circular section of the Nyquist
		# plot ends
		x, y = moving_average(self.get_data('Re')), moving_average(self.get_data('Im'))
		dydx = differentiate(x, y)
		min_index = np.argmin(dydx)
		plt.plot(x[min_index], y[min_index], color='red', label='min')
		return[x[min_index]]


	def semi_circle(self, x_0, x_1, y_1):
		# (x-x_m)^2+y^2=r^2, 
		'''x, y = self.get_data('Re'), self.get_data('Im')
			for i in range(len(x)):
				x_m = np.mean(x[:i])
				r_squared = np.mean((x[:i]-x_m)**2 + y[:i]**2)
				r = r_squared ** 0.5
				print(x_m, r)
		'''
		radius = diameter_estimate(x_0, x_1, y_1) / 2
		x_m = x_0 + radius

		x = np.linspace(x_m - radius, x_m + radius, 250)
		y = np.sqrt(radius**2 - (x-x_m)**2)

		plt.plot(x, y)


	def resistances(self, n=5, ax=plt.gca(), plot=False, **kwargs):
		# This function calculates the line of best fit over every
		# n data points and calculates the x-intercept for each
		# line 
		x 		= self.get_data('Re')
		y 		= self.get_data('Im')

		all_slice_indices = slice_indices(x, n)
		x_intercepts = []

		xs = []
		for slice in all_slice_indices:
			x_slice, y_slice = x[slice], y[slice]
			m, c = line_of_best_fit(x_slice, y_slice)
			x_int = x_intercept(m, c)
			x_intercepts.append(x_int)
			xs.append(np.mean(x_slice))

		if plot:
			ax.plot(xs, x_intercepts, **kwargs)
			ax.set_xlabel(r'Z$_\mathrm{R}$ / $\Omega$')
			ax.set_ylabel(r'Resistance / $\Omega$')

		return x_intercepts


def make_square(ax=plt.gca(), maximum=False):
	# EIS spectra should have square axes
	# This identifies the longest axis and reshapes
	# the other to match
	x1, x2 = ax.get_xlim()
	y1, y2 = ax.get_ylim()
	if not maximum: maximum = max(x2, y2)
	ax.set_xlim([0, maximum])
	ax.set_ylim([0, maximum])


def diameter_estimate(x_0, x_1, y_1):
	# This assumes a circle with a centre which lies
	# on the x-axis
	dx = x_1 - x_0
	dy = y_1
	adj = (dx ** 2 + dy ** 2) ** 0.5
	theta = np.arctan(dy/dx)

	# cos(theta) = adj / diameter
	diameter = adj / np.cos(theta)
	return diameter














