from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

class NMR_1D(NMR_Txt_File_1D):
    def __init__(self, file_path):
        super().__init__(file_path)

    def plot(self, ax=plt.gca(), v_offset=0, **kwargs):
        # Plots the usual intenisty vs ppm, with inverted x-axis
        plot(self.ppm_scale, self.intensities+v_offset, ax=ax, **kwargs)
        ax.set_xlabel('$\delta$ / ppm')
        ax.set_ylabel('Intensity')
        if not ax.xaxis_inverted(): ax.invert_xaxis()

    

