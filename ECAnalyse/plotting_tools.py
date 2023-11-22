import matplotlib.pyplot as plt
import matplotlib as mpl

'''
This little library imports matplotlib for immediate use and also sets a few
stylistic parameters for how graphs should be presented
'''

# This block of code loads some formatting to be used for making the graphs
mpl.rcParams['lines.linewidth'] 				= 2
mpl.rcParams['figure.figsize'] 					= [8.3, 6.225]
mpl.rcParams['axes.linewidth'] 					= 1.2
mpl.rcParams['font.family'] 					= 'Arial'
mpl.rcParams['mathtext.fontset'] 				= 'dejavusans'
mpl.rcParams['font.size'] 						= 24
mpl.rcParams['savefig.dpi'] 					= 300
mpl.rcParams['savefig.format'] 					= 'pdf'
mpl.rcParams['figure.constrained_layout.h_pad'] = 0.2
mpl.rcParams['figure.constrained_layout.w_pad'] = 0.2
mpl.rcParams['figure.constrained_layout.use'] 	= True
mpl.rcParams['legend.labelspacing'] 			= 0.15
mpl.rcParams['axes.xmargin']					= 0.001
mpl.rcParams['axes.prop_cycle'] 				= plt.cycler(color=[
	'black', 'firebrick', 'forestgreen', 'dodgerblue', 'hotpink'])


def integer_x_axis():
	# Changes the tick marks on the x-axis to only be integers. This makes 
	# more sense for graphs where the x-axis is cycle number for example.
	ax = plt.gca()
	ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator())


def plot(x, y, ax=plt.gca(), **kwargs):
	# Plots x and y to a specified axis or if none is specified
	# then to the current axis
	ax.plot(x, y, **kwargs)


def overlay(x, y, ax=plt.gca(), **kwargs):
	# Using the same x-axis, a second y-axis is created to plot
	# the provided x and y datasets to.
	fig = plt.gcf()
	overlay_ax = ax.twinx()
	if len(fig.axes) > 2:
		overlay_ax.spines.right.set_position(('axes', 1. + (len(fig.axes)-2)/4))
	overlay_ax.plot(x, y, **kwargs)


