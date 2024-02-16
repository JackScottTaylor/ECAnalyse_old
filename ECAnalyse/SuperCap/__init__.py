from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *

print('SuperCapacitor Analysis Module Loaded')

class SC_CV(EC_Lab_Txt_File):
    def __init__(self, file_path):
        super().__init__(file_path)

    def specific_cycle_data(self, cycle_indices, *headers):
        # This function takes a list of cycle indices and some header arguments
        # The data is then filtered based on the cycle desired and an array of 
        # the desired datasets are returned as numpy arrys.
        cycle_list = np.unique(self.data['cycle number'])
        cycles = cycle_list[np.array(cycle_indices)]
        hs = list(headers)
        filtered_data = [[] for x in hs]
        for c, *values in zip(self.data['cycle number'], *[self.data[h] for h in headers]):
            if c not in cycles: continue
            for i, v in enumerate(values):
                filtered_data[i].append(v)
        for i, dataset in enumerate(filtered_data): filtered_data[i] = np.array(dataset)
        if len(filtered_data) == 1: return np.array(filtered_data[0])
        return filtered_data


    def plot(self, *cycle_indices, ax=plt.gca(), **kwargs):
        # This lets you do the normal plot for CVs. It also has the option
        # for you to only print certain cycles.
        if list(cycle_indices) != []:
            x, y = self.specific_cycle_data(cycle_indices, 'Ecell/V', '<I>/mA')
        else:
            x, y = self.data['Ecell/V'], self.data['<I>/mA']

        ax.plot(x, y, **kwargs)
        ax.set_xlabel('Voltage / V')
        ax.set_ylabel('Current / mA')


    def charging_step(self, cycle=0):
        # For the chosen cycle, extract the data during the charging regime.
        # Defined as when scan rate is positive
        E, I = self.specific_cycle_data([cycle], 'Ecell/V', '<I>/mA') 
        for i, (E1, E2) in enumerate(zip(E[:-1], E[1:])):
            if E2 < E1:
                end_index = i+1
                break
        return E[:end_index], I[:end_index]
    

    def discharging_step(self, cycle=0):
        # For the chosen cycle, extract the data during the discharging regime.
        # Defined as when scan rate is negative
        E, I = self.specific_cycle_data([cycle], 'Ecell/V', '<I>/mA') 
        for i, (E1, E2) in enumerate(zip(E[:-1], E[1:])):
            if E2 < E1:
                start_index = i
                break
        return E[start_index:], I[start_index:]
    

    def capacitance(self, scan_rate, cycle=0):
        # Uses the current at the voltage mid-point during the charging and
        # discharging step.
        # Scan rate in mVs-1 and current in mA
        # Capacitance in F.
        E, I = self.charging_step(cycle=cycle)
        mid_I = abs(I[len(I) // 2])
        E, I = self.discharging_step(cycle=cycle)
        mid_I += abs(I[len(I) // 2])
        i = mid_I / 2
        return i / scan_rate


    def g_capacitance(self, scan_rate, mass, cycle=0):
        # returns the gravimetric capacitance in Fg-1
        # mass should be in mg
        C = self.capacitance(scan_rate, cycle=cycle)
        return C / (mass / 1000)
    

    

        


    


