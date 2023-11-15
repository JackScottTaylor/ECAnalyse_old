from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('Redox Flow Battery Analysis Module Loaded')


def theoretical_max_charge(concentration, volume, n=1):
	# This function takes a concentration / M and volume / mL and 
	# number of electrons to calculate the charge required to 
	# fully charge the system / mAh

	electron_moles 	= concentration 	* (volume / 1000) * n
	charge_coulombs = electron_moles 	* 96485.3321
	charge_mah 		= charge_coulombs 	/ 3.6
	return charge_mah



class RFB_GCPL(EC_Lab_Txt_File):
	def __init__(self, file_path):
		# This established the RFB_GCPL as a child of the EC_Lab text
		# file class so that data is read in and stored in self.data
		super().__init__(file_path)


	def E_t_plot(self, ax=plt.gca(), **kwargs):
		# Standard plot in this case plots voltage against time
		self.plot('t', 'V', ax=ax, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Voltage / V')


	def add_I_overlay(self, ax=plt.gca(), **kwargs):
		# This is called after E_t_plot to add an overlay of the current
		overlay('t', 'I', ax=ax, **kwargs)
		plt.ylabel('Current / mA')


	def I_t_plot(self, ax=plt.gca(), **kwargs):
		# Plots I vs t
		self.plot('t', 'I', ax=ax, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Current / mA')


	def E_C_plot(self, ax=plt.gca(), **kwargs):
		# Plots battery voltage against capacity

		# If just plot V against C then get horrible straight lines cutting
		# across the plot. To combat this, plot the charging and discharging
		# curves separately. Then it is also necessary to plot for each cycle
		# separately otherwise get annoying lines again.

		for c in self.cycles:
			filter1 = 	{
						'cycle number'	: c,
						'ox/red' 		: 1
						}
			filter2 = 	{
						'cycle number'	: c,
						'ox/red' 		: 0
						}

			E, C = self.filtered_data('E', filter1), self.filtered_data('C', filter1)
			if type(E)!=type(None) and type(C)!=type(None):
				plt.plot(C[:-1], E[:-1], **kwargs)
				# If label given in kwargs, only want one legend entry so this sets
				# the label to not show in legend after one plotting.
				kwargs['label']='_nolegend_'

			E, C = self.filtered_data('E', filter2), self.filtered_data('C', filter2)
			if type(E)!=type(None) and type(C)!=type(None):
				plt.plot(C[1:], E[1:], **kwargs)
				kwargs['label']='_nolegend_'

		plt.xlabel('Capacity / mAh')
		plt.ylabel("Battery Voltage / V")


	def cycle_start_times(self):
		# Returns the start times for each cycle in a narray
		cycles = np.unique(self.data['cycle number'])
		start_times = np.zeros(len(cycles))

		for i, cycle in enumerate(cycles):
			for c, t in zip(self.data['cycle number'], self.data['time/s']):
				if c == cycle:
					start_times[i] = t
					break

		return start_times


	def capacities_charge(self, section='red'):
		# The capacity of a redox flow battery is normally measured from the discharge
		# as this can only come from energy actually stored in the battery. In this case
		# the discharge section is defaulted to when the catholyte is being reduced, but
		# this can be changed using the section key word argument

		if section == 'red':
			section = 0.
		else:
			section = 1.

		cycles 		= np.unique(self.data['cycle number'])
		capacities 	= np.zeros(len(cycles))

		for i, cycle in enumerate(cycles):
			charges = []
			for cycle_n, ox_red, charge in zip(self.data['cycle number'],
				self.data['ox/red'], self.data['(Q-Qo)/mA.h']):
				if cycle_n 	!= cycle 	: continue
				if ox_red 	!= section	: continue
				charges.append(charge)
			if charges != []:
				capacities[i] = max(charges) - min(charges)

		return capacities


	def capacities(self, section='discharge'):
		# This function uses the Q charge and Q discharge variables in the text output file
		# instead of using difference in total charge passed. The value of the capacity is
		# the maximum Q for that cycle which should be correct.
		cycles 		= np.unique(self.data['cycle number'])
		capacities 	= np.zeros(len(cycles))

		charge_data = self.data['Q discharge/mA.h']
		if section == 'charge': charge_data = self.data['Q charge/mA.h']

		for i, cycle in enumerate(cycles):
			cycle_charges = []
			for cycle_num, charge in zip(self.data['cycle number'], charge_data):
				if cycle_num < cycle: continue
				if cycle_num > cycle: break
				cycle_charges.append(charge)
			capacities[i] = max(cycle_charges)
		return capacities


	def coloumbic_efficiencies(self):
		# Coulombic efficiency defined here as (discharge Q / charge Q) * 100%
		charge_cap 		= self.capacities(section='charge')
		discharge_cap 	= self.capacities(section='discharge')
		efficiencies 	= np.divide(discharge_cap, charge_cap) * 100
		return efficiencies


	def efficiency(self, x='cycles', **kwargs):
		efficiencies = self.coloumbic_efficiencies()
		start_times = self.cycle_start_times()

		if x == 'time':
			plt.plot(start_times, efficiencies, **kwargs)
			plt.xlabel('Time / s')
		else:
			plt.plot(efficiencies, **kwargs)
			plt.xlabel('Cycle')
		plt.ylabel('Coloumbic Efficiency / %')
		plt.ylim(0, 100)


	def capacities_vs_cycles(self, section='discharge', scale=1, **kwargs):
		capacities = self.capacities(section=section) * scale
		plt.plot(capacities, **kwargs)
		plt.xlabel('Cycle Number')
		plt.ylabel('Capacity / mAh')
		integer_x_axis()


	def capacities_vs_time(self, section='discharge', scale=1, **kwargs):
		capacities = self.capacities(section=section) * scale
		start_times = self.cycle_start_times()
		plt.plot(start_times, capacities, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Capacity / mAh')


	def capacity_fade(self):
		# Plots the capacity fade as a function of time using the start times of the 
		# cycles.
		x = self.cycle_start_times() / 3600
		y = self.capacities()

		dydx = differentiate(x, y)
		plt.plot(x, (dydx / y) * 100)

		plt.xlabel('Time / h')
		plt.ylabel('Capacity Fade / % h$^{-1}$')


	def capacity_retention(self):
		# Plots the capacity retention as a function of time using the start times of
		# the cycles.

		x = self.cycle_start_times() / 3600
		y = self.capacities()

		dydx = differentiate(x, y)
		plt.plot(x, 100 + (dydx / y) * 100)

		plt.xlabel('Time / h')
		plt.ylabel('Capacity Fade / % h$^{-1}$')
		






