from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('SC_CC Loaded')

class SCCC_Gas(csv_reader):
	def __init__(self, file_path):
		Super()__init__(file_path)

		self.smoothed_data = {'string': [1, 2, 3, 4]}

	def standard_plot(self):
		x = self.data['time/s']
		y = self.data['Pressure/bar (on Analog In1)']
		plt.plot(x,y)

    def export_smoothed_data_as_txt(self, headers, n, file_name):
    	# headers is list of data headers to export
		smoothed_data = {}
		for header in headers:
			data = self.data[header]
			smoothed = moving_average(data, n=n)
			smoothed_data[header] = smoothed

		