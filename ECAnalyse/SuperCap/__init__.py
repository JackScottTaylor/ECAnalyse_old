from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('SuperCapacitor Analysis Module Loaded')

class SC_CV(EC_Lab_Txt_File):
    def __init__(self, file_path):
        super().__init__(file_path)

    def plot(self, ax=plt.gca(), **kwargs):
        x, y = self.data['Ecell/V'], self.data['<I>/mA']
        ax.plot(x, y, **kwargs)
        ax.set_xlabel('Voltage / V')
        ax.set_ylabel('Current / mA')


