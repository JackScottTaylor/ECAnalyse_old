from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

from scipy.signal import find_peaks, peak_prominences

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

	def scale_current(self, factor):
		# This function scales the current data by a factor.
		self.data['<I>/mA'] = self.data['<I>/mA'] * factor

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

	def smooth_EI(self, n=3):
		# This function smooths the potential and current data using
		# a moving average over n points. This cannot be undone.
		self.data['Ewe/V'] = moving_average(self.data['Ewe/V'], n=n)
		self.data['<I>/mA'] = moving_average(self.data['<I>/mA'], n=n)


	def ox_red_section(self, section, cycle=-1):
		# This function returns E, I for the specified section (ox or red)
		# of the specified cycle
		if section not in ['ox', 'red']:
			raise ValueError("Section must be 'ox' or 'red'")
		# Identify data relating to cycle number, E and I
		cycles, Es, Is = self.data['cycle number'], self.data['Ewe/V'], self.data['<I>/mA']
		# Identify the cycle numbers
		cycle_set = set(cycles)
		# Convert cycle in to a number in the range of the cycle set. This way, 
		# cycle can be negative and will still be valid.
		specified_cycle = float(cycle % len(cycle_set)) + 1.0
		E_sec, I_sec = [], []
		# To determine direction of scan, have to compare potential to next value.
		for i in range(len(cycles[:-1])):
			# If cycle too low, continue.
			# If cycle too high, then break.
			c = cycles[i]
			if c < specified_cycle: continue
			if c > specified_cycle: break
			# Determine scan direction. If correct then append E, I to the lists.
			sec = 'ox' if Es[i] < Es[i+1] else 'red'
			if sec != section: continue
			E_sec.append(Es[i])
			I_sec.append(Is[i])
		# Return the E, I data as numpy arrays.
		return np.array(E_sec), np.array(I_sec)
	

	def ox_section(self, cycle=-1):
		# This function returns E, I for the oxidation section of the specified cycle
		return self.ox_red_section('ox', cycle=cycle)
	

	def red_section(self, cycle=-1):
		# This function returns E, I for the reduction section of the specified cycle
		return self.ox_red_section('red', cycle=cycle)
	
	
	def peaks(self, section, cycle=-1, n=2):
		# This function first extaracts the correct section (ox or red) of the
		# specified cycle. Then it finds the n most prominent peaks and returns
		# the peaks as a list of the potentials and a list of the currents.
		E, I = self.ox_red_section(section, cycle=cycle)
		if section == 'red': I = -I
		peaks, _ = find_peaks(I)
		prominences = peak_prominences(I, peaks)[0]
		sorted_peaks = np.argsort(prominences)
		peak_Es = E[peaks[sorted_peaks[-n:]]]
		peak_Is = I[peaks[sorted_peaks[-n:]]]
		if section == 'red': peak_Is = -peak_Is
		return peak_Es, peak_Is
	

	def ox_peaks(self, cycle=-1, n=2):
		# This function returns the n most prominent oxidation peaks
		return self.peaks('ox', cycle=cycle, n=n)
	
	
	def red_peaks(self, cycle=-1, n=2):
		# This function returns the n most prominent reduction peaks
		return self.peaks('red', cycle=cycle, n=n)
	









