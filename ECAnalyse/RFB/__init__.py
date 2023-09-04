from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('Redox Flow Battery Analysis Module Loaded')

class RFB_GCPL(EC_Lab_Txt_File):
	def __init__(self, file_path):
		# This established the RFB_GCPL as a child of the EC_Lab text
		# file class so that data is read in and stored in self.data
		super().__init__(file_path)

	def standard_plot(self, **kwargs):
		# Standard plot in this case plots voltage against time
		x = self.data['time/s']
		y = self.data['Ewe/V']
		plt.plot(x, y, **kwargs)
		plt.xlabel('Time / s')
		plt.ylabel('Voltage / V')

	def reduction_charge_by_cycle