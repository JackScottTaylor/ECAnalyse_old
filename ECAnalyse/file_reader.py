import numpy as np
from .plotting_tools import *

class EC_Lab_Txt_File:
	# This class is simply used to read in an EC_Lab exported .txt file and store all of the relevant data as numpy arrays.
	
	def __init__(self, file_path):
		self.data_names 	= []
		self.data         	= {}

		# The first line contains some mus and therefore is encoded with latin1
		# instead of the usual UTF-8
		with open(file_path, encoding='latin1') as file:
			self.data_names = file.readline().split('\t')

			# For ease, replacing µ with u in the data_names
			self.data_names = [x.replace('µ', 'u') for x in self.data_names]

			# Assign an empty list to each of the data names
			for name in self.data_names: self.data[name] = []

			# Convert each value into a float and append to correct list
			for line in file.readlines()[1:]:
				values = line.split('\t')
				for value, name in zip(values, self.data_names):
					self.data[name].append(float(value))

		# Convert the strings of floats into numpy arrays
		for name in self.data_names: self.data[name] = np.array(self.data[name])

		if 'cycle number' in self.data.keys():
			self.cycles = np.unique(self.data['cycle number'])
		else:
			self.cycles = np.array([])

		self.abbreviations = {
				't' 			: 'time/s',
				'dq' 			: 'dq/ma.h',
				'Q' 			: 'Q-Qo)/mA.h',
				'E' 			: 'Ewe/V',
				'C_Charge'		: 'Capacitance charge/µF',
				'C_Discharge' 	: 'Capacitance discharge/µF',
				'I' 			: '<I>/mA',
				'C' 			: 'Capacity/mA.h',
				'efficiency' 	: 'Efficiency/%',
				}	

	def get_data(self, x):
		if x not in self.abbreviations.keys(): return self.data[x]
		return self.data[self.abbreviations[x]]


	def plot(self, x, y, ax=plt.gca(), **kwargs):
		x = self.get_data(x)
		y = self.get_data(y)
		plot(x, y, ax=ax, **kwargs)


	def overlay(self, x, y, ax=plt.gca(), **kwargs):
		x = self.get_data(x)
		y = self.get_data(y)
		overlay(x, y, ax=ax, **kwargs)


	def filtered_data(self, data, filter_dict):
		'''
		data is a key word to retrieve one of the data sets from self.data
		filter_dict contains dataset keywords as its own keywords
		the attached value is the filter value for the data set.
		The filtered data is then returned as a numpy array
		'''

		filtered_data = []
		data_vars = filter_dict.keys()
		full_data = {}
		for var in data_vars:
			full_data[var] = self.get_data(var)

		for i, x in enumerate(self.get_data(data)):
			qualifies = True
			for var in data_vars:
				if full_data[var][i] != filter_dict[var]:
					qualifies = False
					break
			if qualifies: filtered_data.append(x)

		return np.array(filtered_data)



	def data_from_cycle(self, data, cycle):
		if cycle not in self.cycles: return []
		specific_data = []
		for c, d, in zip(self.data['cycle number'], self.get_data(data)):
			if c == cycle:
				specific_data.append(d)
			if c > cycle:
				return np.array(specific_data)


class EC_Lab_CSV_File:
	def __init__(self, file_path):
		self.data_names 	= []
		self.data         	= {}

		with open(file_path, encoding='latin1') as file:
			file.readline()
			self.data_names = file.readline().replace('"', '').split(';')

			# For ease, replacing µ with u in the data_names
			self.data_names = [x.replace('µ', 'u') for x in self.data_names]

			# Assign an empty list to each of the data names
			for name in self.data_names: self.data[name] = []

			# Convert each value into a float and append to correct list
			for line in file.readlines()[2:]:
				values = line.split(';')
				for value, name in zip(values, self.data_names):
					self.data[name].append(float(value))

		# Convert the strings of floats into numpy arrays
		for name in self.data_names: self.data[name] = np.array(self.data[name])

		
