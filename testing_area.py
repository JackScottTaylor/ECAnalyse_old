from ECAnalyse.RFB import *
from ECAnalyse.SuperCap import *

file1 = RFB_GCPL('/Users/jack/Documents/Experiments/029 Redox Flow Batteries/2,7-AQDS 1M KCl 22 August 2023/2,7-AQDS 0,1M in 1M KCl solution, ferrocyanide 0,25M catholyte_C01.txt')
file1.standard_plot(label='File1')
file2 = RFB_GCPL('/Users/jack/Documents/Experiments/029 Redox Flow Batteries/2,7-AQDS 1M KCl 22 August 2023/2,7-AQDS 0,1M in 1M KCl solution, ferrocyanide 0,25M catholyte (restart)_C01.txt')
file2.standard_plot(label='File2')
plt.legend()
plt.show()