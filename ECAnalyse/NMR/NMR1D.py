'''
Contains class for handling 1D NMR
'''

from ..file_reader import NMR_Txt_File_1D
from ..plotting_tools import *

from ..analysis_tools import differentiate

from scipy.signal import find_peaks

def txt_to_ppm_intensities(txt_file):
    # Use file reader to extract ppm_scale and spectra
    # from .txt file
    file = NMR_Txt_File_1D(txt_file)
    return file.ppm_scale, file.intensities

class NMR:
    # Class for performing operations on a 1D NMR spectra
    # Defined only by ppm scale and intensitites
    def __init__(self, ppm_scale, intensities):
        self.ppm_scale = ppm_scale
        self.intensities = intensities

    def plot(self, ax=plt.gca(), v_offset=0, **kwargs):
        # Plots the usual intensity vs ppm, with inverted xaxis
        ax.plot(self.ppm_scale, self.intensities+v_offset, **kwargs)
        ax.set_xlabel('$\delta$ / ppm')
        ax.set_ylabel('Intensity')
        # Check to see whether x-axis already inverted, if not then invert
        if not ax.xaxis_inverted(): ax.invert_xaxis()

    def peaks(self, height=0.05):
        # Use scipy find_peaks to locate all peaks above a threshold
        # defined as the maximum intensity * height
        # height therefore should be a float between 0 and 1.
        thresh = height * max(self.intensities)
        peaks, _ = find_peaks(self.intensities, height=thresh)
        return peaks
    
    def differentiated(self):
        # Returns d(intensity) / d(ppm)
        return differentiate(self.ppm_scale, self.intensities)
    
    def differentiated_peaks(self, prominence=5):
        # Find the local maxima with a set prominence in the
        # derivative of intensity
        prominence = prominence * 10 ** 6
        maxima, _ = find_peaks(self.differentiated(), prominence=prominence)
        minima, _ = find_peaks(-self.differentiated(), prominence=prominence)
        return maxima, minima
    
    def fit_differentiated_lorentzians(self, prominence):
        y = self.differentiated()
        maxima, minima = self.differentiated_peaks(prominence=prominence)
        x_intercepts = [(self.ppm_scale[m1]+self.ppm_scale[m2])/2 for m1, m2 in zip(maxima, minima)]
        





