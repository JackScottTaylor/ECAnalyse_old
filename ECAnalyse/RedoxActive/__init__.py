from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print("Redox Active Molecule Module Loaded")

def CV_axis_labels(ref=''):
	# This function adds the normal axis labels. If a reference is used
	# then this should be specified and it will be stated that the
	# potential is referenced against this value.
	plt.ylabel('Current / mA')
	if ref:
		plt.xlabel(f'Potential / V vs {ref}')
	else:
		plt.xlabel('Applied Potential / V')


class RA_CV(EC_Lab_Txt_File):
	def __init__(self, file_path):
		super().__init__(file_path)

		self.number_of_cycles = len(np.unique(self.data['cycle number']))

	def apply_reference(self, ref):
		# Often CVs are plotted with the potential being
		# referenced against a standard potential. This 
		# function applies a translation to the potential
		# data stored in self.data[Ewe/V]
		self.data['Ewe/V'] = self.data['Ewe/V'] - ref

	def plot(self, **kwargs):
		# Most usually just want to plot current against
		# potential
		x, y = self.data['Ewe/V'], self.data['<I>/mA']
		plt.plot(x, y, **kwargs)
		plt.xlabel('Applied Potential / V')
		plt.ylabel('Current / mA')

	def plot_cycles(self, *cycle_indices, **kwargs):
		# This function allows the user to plot only certain cycles of
		# the CV by adding the wanted cycle indices as arguments.
		cycle_list = np.unique(self.data['cycle number'])
		cycles = cycle_list[np.array(cycle_indices)]
		x, y = [], []
		for c, E, I in zip(self.data['cycle number'], self.data['Ewe/V'], self.data['<I>/mA']):
			if c not in cycles: continue
			x.append(E)
			y.append(I)
		plt.plot(x, y, **kwargs)

	def plot_each_cycle(self, **kwargs):
		# Plots each of the cycles individually and
		# labels them
		for i in range(self.number_of_cycles):
			self.plot_cycles(i, label=f'Cycle {i+1}', **kwargs)

	def smooth_EI(self, n=3):
		# This function smooths the potential and current data using
		# a moving average over n points. This cannot be undone.
		self.data['Ewe/V'] = moving_average(self.data['Ewe/V'], n=n)
		self.data['<I>/mA'] = moving_average(self.data['<I>/mA'], n=n)



