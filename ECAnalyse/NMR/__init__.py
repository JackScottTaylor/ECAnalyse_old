from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

from scipy.signal import find_peaks
from scipy.optimize import curve_fit

class NMR_1D(NMR_Txt_File_1D):
    def __init__(self, file_path):
        super().__init__(file_path)

    def plot(self, ax=plt.gca(), v_offset=0, **kwargs):
        # Plots the usual intenisty vs ppm, with inverted x-axis
        plot(self.ppm_scale, self.intensities+v_offset, ax=ax, **kwargs)
        ax.set_xlabel('$\delta$ / ppm')
        ax.set_ylabel('Intensity')
        if not ax.xaxis_inverted(): ax.invert_xaxis()

    def peaks(self, height=0.05):
        thresh = height * max(self.intensities)
        peaks, _ = find_peaks(self.intensities, height=thresh)
        return peaks
    
    def n_highest_peaks(self, n):
        # Instead of returning the indices of all peaks above a 
        # certain threshold, this function returns the indices
        # of the n highest peaks
        peaks, _ = find_peaks(self.intensities)
        n_highest = peaks[np.argsort(self.intensities[peaks])[-n:]]
        return n_highest
    
    def label_peaks(self, height=0.05):
        peaks = self.peaks(height=height)
        v_offset = max(self.intensities) / 10
        for peak in peaks:
            x = [self.ppm_scale[peak], self.ppm_scale[peak]]
            y = [self.intensities[peak] + 1 * v_offset,
                 self.intensities[peak] + 3 * v_offset,]
            plt.plot(x, y, color='black', linewidth=1)

    def deconvolute_lorentzian(self, n=0, height=0.05):
        if n != 0:
            peaks = self.n_highest_peaks(n)
        else:
            peaks = self.peaks(height=height)

        def sum_of_lorentzians(x, *params):
            results = np.zeros_like(x)
            for i in range(0, len(params), 3):
                amplitude, center, width = params[i:i+3]
                results += amplitude / (1 + ((x - center) / (width / 2))**2)
            return results
        
        initial_guess = []
        for peak in peaks:
            initial_guess += [self.intensities[peak], self.ppm_scale[peak], 0.005]

        params, covariance = curve_fit(sum_of_lorentzians, self.ppm_scale,
                                       self.intensities, p0=initial_guess,
                                       maxfev=100000)
        return params

    def deconvolute_gaussian(self, height=0.05):
        peaks = self.peaks(height=height)

        def sum_of_gaussians(x, *params):
            results = np.zeros_like(x)
            for i in range(0, len(params), 3):
                amplitude, mean, stddev = params[i:i+3]
                results += amplitude * np.exp(-(x - mean)**2 / (2 * stddev**2))
            return results
        
        initial_guess = []
        for peak in peaks:
            initial_guess += [self.intensities[peak], self.ppm_scale[peak], 0.002]

        params, covariance = curve_fit(sum_of_gaussians, self.ppm_scale,
                                       self.intensities, p0=initial_guess,
                                       maxfev=10000)
        return params
    
    def integration(self, total=100):
        integral = np.cumsum(self.intensities) 
        return integral * total / integral[-1]

    
    
        





    

