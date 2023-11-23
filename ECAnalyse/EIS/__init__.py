from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print("Ready to Analyse EIS!!")

class EIS(EC_Lab_Txt_File):
	def __init__(self, file_path):
		super().__init__(file_path)

	def Nyquist(self, ax=plt.gca(), **kwargs):
		self.plot('Re', 'Im', ax=ax, **kwargs)
		ax.set_xlabel(r'Re(Z)/$\Omega$')
		ax.set_ylabel(r'Im(Z)/$\Omega$')

	def linear_section(self, section=0.9, plot=False, ax=plt.gca(), **kwargs):
		# section determines how much of first part to ignore. Preset to use
		# last 10% of data to generate linear section.
		start_index = int(((len(self.get_data('Re')) - 1) * section) // 1)
		x, y = self.get_data('Re')[start_index:], self.get_data('Im')[start_index:]
		m, c = line_of_best_fit(x, y)
		if plot:
			x1, x2 = ax.get_xlim()
			ax.plot([x1, x2], [m*x1+c, m*x2+c], **kwargs)
		return m, c

	def Bode_Z(self, ax=plt.gca(), **kwargs):
		x = np.log(self.get_data('freq/Hz'))
		Re, Im = self.get_data('Re'), self.get_data('Im')
		absolute_Z = np.sqrt(np.add(np.multiply(Re, Re), np.multiply(Im, Im)))
		arg_z = np.arctan(np.divide(Im, Re))
		ax.set_xlabel(r'ln($\omega$ / Hz)')
		ax.set_ylabel('ln(|Z| / $\Omega$)')
		plot(x, np.log(absolute_Z), **kwargs)

	def Bode_arg(self, ax=plt.gca(), **kwargs):
		x = np.log(self.get_data('freq/Hz'))
		Re, Im = self.get_data('Re'), self.get_data('Im')
		absolute_Z = np.sqrt(np.add(np.multiply(Re, Re), np.multiply(Im, Im)))
		arg_Z = np.arctan(np.divide(Im, Re))
		ax.set_xlabel(r'ln($\omega$ / Hz)')
		ax.set_ylabel('Arg(Z) / Radians')
		plot(x, arg_Z, **kwargs)

	def Bode(self, ax=plt.gca()):
		self.Bode_Z(ax=ax)
		overlay_ax = ax.twinx()
		self.Bode_arg(ax=overlay_ax, color='firebrick')
		overlay_ax.spines['right'].set_color('firebrick')
		overlay_ax.yaxis.label.set_color('firebrick')
		overlay_ax.tick_params(axis='y', colors='firebrick')



def make_square(ax=plt.gca(), maximum=False):
	# EIS spectra should have square axes
	# This identifies the longest axis and reshapes
	# the other to match
	x1, x2 = ax.get_xlim()
	y1, y2 = ax.get_ylim()
	if not maximum: maximum = max(x2, y2)
	ax.set_xlim([0, maximum])
	ax.set_ylim([0, maximum])





