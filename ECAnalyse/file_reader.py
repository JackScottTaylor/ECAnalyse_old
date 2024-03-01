import numpy as np
from .plotting_tools import *

def replace_escape_seqs(string):
	esc_dict = {
				'\a' : r'\a',
				'\b' : r'\b',
				'\f' : r'\f',
				'\n' : r'\n',
				'\r' : r'\r',
				'\t' : r'\t',
				'\v' : r'\v'
	}
	new_string = ''
	for char in string:
		if char in esc_dict.keys():
			new_string += esc_dict[char]
		else:
			new_string += char
	return new_string


class EC_Lab_Txt_File:
	# This class is simply used to read in an EC_Lab exported .txt file and store all
	# of the relevant data as numpy arrays.
	
	def __init__(self, file_path):
		self.data_names 	= []
		self.data         	= {}

		# For those pesky Windows users, this gets rid of most escape characters
		# that can be passed in file paths, however can't handle if path contains
		# \N, \U, \u, \x. Best practise for windows users is to use r'' string
		# format for copy and pasting file paths.
		file_path = replace_escape_seqs(file_path)

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


class NMR_Txt_File_1D:
	# Used for reading 1D NMR output by topspin
	def __init__(self, filePath):
		self.intensities = []

		with open (filePath) as file:
			for line in file.readlines():
				if line[0] != '#':
					self.intensities.append(float(line.strip()))
					continue

				if 'LEFT' in line:
					ppm_max, ppm_min = line.split()[3], line.split()[7]
					ppm_max, ppm_min = float(ppm_max), float(ppm_min)
					continue

				if 'SIZE' in line:
					size = int(line.split()[3])
					
		self.ppm_scale = np.linspace(ppm_max, ppm_min, size)
		self.intensities = np.array(self.intensities)
				
			
class NMR_Txt_File_2D:
	# Used for reading 2D NMR output by topspin
	def __init__(self, filePath):
		self.intensities = []

		with open(filePath) as file:
			data = []
			for line in file.readlines():
				if line[0] != '#':
					data.append(float(line.strip()))
					continue

				if '# row' in line:
					self.intensities.append(np.array(data))
					data = []
					continue

				if 'F2LEFT' in line:
					ppm_max, ppm_min = line.split()[3], line.split()[7]
					ppm_max, ppm_min = float(ppm_max), float(ppm_min)
					continue

				if 'NROWS' in line:
					nrows = int(line.split()[3])
					continue

				if 'NCOLS' in line:
					ncols = int(line.split()[3])
					continue
			
			self.intensities.append(np.array(data))

		self.intensities = np.array(self.intensities[1:])
		self.spectra = self.intensities
		self.ppm_scale = self.ppm_scale = np.linspace(ppm_max, ppm_min, ncols)

				

			
					

