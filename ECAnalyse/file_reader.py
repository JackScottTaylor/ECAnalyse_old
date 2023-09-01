import numpy as np

class EC_Lab_Txt_File:
	# This class is simply used to read in an EC_Lab exported .txt file and store all of the relevant data as numpy arrays.
	
	def __init__(self, file_path):
		self.data_headers 	= []
		self.data         	= {}

		# The first line contains some mus and therefore is encoded with latin1
		# instead of the usual UTF-8
		with open(txtFile, encoding='latin1') as file:
			self.data_names = file.readline().split('\t')

			# For ease, replacing µ with u in the data_names
			self.data_names = [x.replace('µ', 'u') for x in self.data_names]

			# Assign an empty list to each of the data names
			for name in self.data_headers: self.data[name] = []

			# Convert each value into a float and append to correct list
			for line in file.readlines()[1:]:
				values = line.split('\t')
				for value, name in zip(values, self.data_names):
					self.data[name].append(float(value))

		# Convert the strings of floats into numpy arrays
		for name in self.data_names: self.data[name] = np.array(self.data[name])



class EC_Lab_Csv_File:
	def __init__(self, file_path):
		self.data_headers 	= []
		self.data         	= {}
