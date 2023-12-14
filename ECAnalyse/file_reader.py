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
			for line in file.readlines():
				values = line.split('\t')
				for value, name in zip(values, self.data_names):
					self.data[name].append(float(value))

		# Convert the strings of floats into numpy arrays
		for name in self.data_names: self.data[name] = np.array(self.data[name])

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
				'Re' 			: 'Re(Z)/Ohm',
				'Im' 			: '-Im(Z)/Ohm'
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

		
