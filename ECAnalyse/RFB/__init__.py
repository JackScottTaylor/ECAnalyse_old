from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('Redox Flow Battery Analysis Module Loaded')

class RFB_GCPL(EC_Lab_Txt_File):
	def __init__(self, file_path):
		# This established the RFB_GCPL as a child of the EC_Lab text
		# file class so that data is read in and stored in self.data
		super().__init__(file_path)


	def plot(self, **kwargs):
		# Standard plot in this case plots voltage against time
		x = self.data['time/s']
		y = self.data['Ewe/V']
		plt.plot(x, y, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Voltage / V')


	def theoretical_max_charge(self, concentration, volume, n=1):
		# This function takes a concentration / M and volume / mL and 
		# number of electrons to calculate the charge required to 
		# fully charge the system / mAh

		electron_moles 	= concentration 	* (volume / 1000) * n
		charge_coulombs = electron_moles 	* 96485.3321
		charge_mah 		= charge_coulombs 	/ 3.6
		return charge_mah


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


	def capacities_vs_cycles(self, section='discharge', **kwargs):
		capacities = self.capacities(section=section)
		plt.plot(capacities, **kwargs)
		plt.xlabel('Cycle Number')
		plt.ylabel('Capacity / mAh')


	def capacities_vs_time(self, section='discharge', **kwargs):
		capacities = self.capacities(section=section)
		start_times = self.cycle_start_times()
		plt.plot(start_times, capacities, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Capacity / mAh')






