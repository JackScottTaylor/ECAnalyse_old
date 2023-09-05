from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('SC_CC Loaded')

class SCCC_Gas(csv_reader):
	def __init__(self, file_path):
		Super()__init__(file_path)

	def standard_plot(self):
		x = self.data['time/s']
		y = self.data['Pressure/bar (on Analog In1)']