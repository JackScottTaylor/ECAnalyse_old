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
mpl.rcParams['font.family'] 					= 'Times New Roman'
mpl.rcParams['font.size'] 						= 24
mpl.rcParams['savefig.dpi'] 					= 300
mpl.rcParams['savefig.format'] 					= 'pdf'
mpl.rcParams['figure.constrained_layout.h_pad'] = 0.2
mpl.rcParams['figure.constrained_layout.w_pad'] = 0.2
mpl.rcParams['figure.constrained_layout.use'] 	= True
mpl.rcParams['legend.labelspacing'] 			= 0.15
mpl.rcParams['axes.prop_cycle'] 				= plt.cycler(color=[
	'black', 'firebrick', 'forestgreen', 'dodgerblue', 'hotpink'])