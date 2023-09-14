from ..analysis_tools import *
from ..file_reader import *
from ..plotting_tools import *
import os

class SuperCap_GCD(EC_Lab_Txt_File):
	def __init__(self, file_path):
		# This established the SuperCap_GCD as a child of the EC_Lab text
		# file class so that data is read in and stored in self.data
		super().__init__(file_path)

	def getall(self):

		import numpy as np            #necessary initialisation stuff
		import matplotlib.pyplot as plt
		from scipy.stats import linregress
		pathway=input('what is the pathway? (when you upload the file, right click and copy path) ')
		currentdensity=input('what is the current density in A/g? ')
		currentdensity=float(currentdensity)
		current=float(input('what is the mass of the electrode in mg? '))*currentdensity*0.001
		cycles=int(input('How many cycles have you inputted? '))
		peakvoltage=float(input('what is the peak voltage? e.g. O.8V 1.0V? '))
		steps=int(input('How many steps in the gradient would you like to take? '))


		time= self.data['time/s']
		voltage = self.data['<Ewe>/V']
		uneditedtime=time       #the time array will be edited and cut off along the way in the code. Unedited time will stay the same.
		uneditedvoltage=voltage   #the voltage array will be edited and cut off along the way in the code. Unedited voltage will stay the same.
		size=np.prod(time.shape) #size of the array, will be used later on a lot (how many data points)
		dVdt= []
		#need to now differentiate between vertical and diagonal line
		#use derivatives
		#use a loop
		for j in np.arange(1,size//steps, 1): #calculates gradient every 'steps' number of points
		  derivative=(voltage[steps*j]-voltage[steps*(j-1)])/(time[steps*j]-time[steps*(j-1)])
		  dVdt.append(derivative)
		#the loop above works out the derivative between every 'steps' points and adds it to an array called dVdt which stores all the gradients
		plt.plot(time,voltage)
		plt.xlabel('Time/s')
		plt.ylabel('Voltage/V')
		plt.title('GCD you inputted') #plots the GCD
		plt.show()
		lengthofdVdt=len(dVdt)
		remainder= np.prod(time.shape) % steps #let's say you take every 5 points but you have 7 points overall. This removes the last 2 points temporarily so that the gradient can be plotted
		if remainder>0:
		    remaindertime=time[:-remainder]
		else:
		    remaindertime=time
		gradtime=remaindertime[::steps]
		plt.plot(gradtime[:-1],dVdt)
		plt.xlabel('Time/s')
		plt.ylabel('Rate of change of Voltage/Vs\u207b\u00b9 ')
		plt.title('dVdt graph for whole GCD')     #plots the gradient function over the whole GCD
		plt.show()
		dischargev = {}   #messy array stuff.. dischargev,t,dVdt stores the full discharge curve for every cycle. Verticalv,t,dVdt stores every vertical section for every cycle
		discharget = {}   #diagonalv,t,dVdt stores every diagonal section for every cycle (voltage, time and rate of change in voltage(dV/dt))
		dischargedVdt = {}
		verticaldVdt = {}
		verticalt = {}
		verticalv= {}
		diagonaldVdt = {}
		diagonalt = {}
		diagonalv= {}
		capacity = {}   #will store capacity for every cycle number
		capacitance= {} #stores Capacitance for every cycle number
		fullcapacitance= {}
		IRdrop= {}
		ESR = {}
		endofcycle=0
		for cyclenumber in np.arange(0, cycles, 1): #repeats for every cycle
		    dVdt = dVdt[endofcycle:]    #removes the previous cycle it analysed from the data that is yet to be analysed, effectively moving on to analyse the next cycle
		    time = time[steps * endofcycle:]
		    voltage = voltage[steps * endofcycle:]
		    investigate = dVdt[:lengthofdVdt // (cycles + 1)] #needs to find the initial vertical drop. Which corresponds to the minimum in gradient. However that's only within the cycle.
		    # So we have to make it such that it only takes the data from the cycle it is analysing. Let's say there are 4 cycles, we know that in the first 1/5 of the total data, the 
		    # first minima will be in there. when it repeats, it removes the first cycle. so now it tests the second cycle... etc

		    beginningofdischarge = np.argmin(investigate)      #removes any charging and a bit of the voltage drop, makes it easier to find the end of the voltage drop

		    voltage = voltage[steps * (beginningofdischarge):] #edits the voltage to remove the charging part and keep only the discharge part
		    time = time[steps * (beginningofdischarge):]
		    dVdt = dVdt[beginningofdischarge:]

		    for endofcycle, loop in enumerate(dVdt):  # removes any of the charging part that may come after the diagonal line
		        if endofcycle >= (len(dVdt)-1) or loop > 0.00:
		            dischargev[cyclenumber] = voltage[:steps * (endofcycle)]  #removes charging part from the array
		            discharget[cyclenumber] = time[:steps * (endofcycle)]
		            dischargedVdt[cyclenumber] = dVdt[:endofcycle]
		            break
		    temporaryv = dischargev[cyclenumber]  #temporaryv,t,dVdt are needed because the dischargev,t,dVdt are dictionaries. Think of them as a table made of rows and columns and each 
		    #column corresponds to the dischargev,t,dVdt for each cycle. To edit the values in the column, we need an array because we use array cutting methods throughout this analysis
		    #whenever we use something like voltage=voltage[:something] this is cropping an array. So we take each column in the dict and make it an array and then edit that array. Then
		    #equal that array back to the column in the dict.
		    temporaryt = discharget[cyclenumber]
		    temporarydVdt = dischargedVdt[cyclenumber]


		    #METHOD OF FINDING IR DROP
		    #Current method used is to take the gradient of the full discharge section and find it's mean.
		    # We see a spike that corresponds to the Ir drop and a relatively flat, horizontal line which corresponds to the diagonal section.
		    # The mean will be effectively the y value of the flat line and sp when the gradient first goes to this value, we consider any subsequent data as the diagonal section 
		    # and any section before it as the vertical, IR drop, part.
		    threshold = np.mean(temporarydVdt) #mean of gradient of discharge part
		    for i1, loop in enumerate(temporarydVdt): #finds the end of the voltage drop by finding when the gradient goes above the mean
		        if 0 > loop > threshold:
		            endofIRdrop = i1 #endofIRdrop becomes the index corresponding to what position in the dVdt array it is when it goes above the mean
		            break
		    verticaldVdt[cyclenumber] = temporarydVdt[:endofIRdrop] #removes any discharge part that's associated with the diagonal section so only the vertical section remains
		    verticalt[cyclenumber] = temporaryt[:steps * endofIRdrop]
		    verticalv[cyclenumber]= temporaryv[:steps * endofIRdrop]
		    diagonaldVdt[cyclenumber] = temporarydVdt[endofIRdrop:] #removes any discharge part that's associated with the vertical section so only the diagonal section remains
		    diagonalt[cyclenumber] = temporaryt[steps * endofIRdrop:]
		    diagonalv[cyclenumber] = temporaryv[steps * endofIRdrop:]
		    temporaryt=diagonalt[cyclenumber] #The diagonal section needs to be analysed when working out capacity. We need to make the time and voltage values associated with the cycle
		    #into an array so we can take the last and first value out. We can't do this with diagonalt as it's a dict not an array. Imagine it as a book, chapters and pages:
		    #you can only state the book and what chapter it is (dict and what column) and not the page as well. However making it an array basically keeps only the chapter 
		    #and then you can state which page in the chapter it is in. 
		    temporaryv=diagonalv[cyclenumber]
		    vertical = temporaryv[0]  #end of vertical IR drop
		    slope, intercept, _, _, _ = linregress(diagonalt[cyclenumber], diagonalv[cyclenumber]) #works out slope of discharge and therefore the capacitance

		    capacity[cyclenumber] = 0.5 * currentdensity * (temporaryt[-1] - temporaryt[0])  #works out capacity
		    capacitance[cyclenumber]= -2 * currentdensity / slope #equation cancels out the masses: assumes both electrodes have the same mass. then since m1+m2=2*m1=2*m2 then (m1+m2)/m is 2
		    IRdrop[cyclenumber]= peakvoltage - vertical
		    ESR[cyclenumber]= (peakvoltage - vertical) / (2 * current)
		    fullcapacitance[cyclenumber]=-2*currentdensity*(temporaryt[-1]-temporaryt[0])/(temporaryv[-1]-temporaryv[0])


		capacity_values=list(capacity.values())
		capacitance_values = list(capacitance.values())
		cycle_numbers = list(capacitance.keys())
		IRdrop_values = list(IRdrop.values())
		ESR_values= list(ESR.values())
		fullcapacitance_values= list(fullcapacitance.values())
		#plots Capacitance against cycle number
		plt.plot(cycle_numbers, capacitance_values)
		plt.xlabel('Cycle number')
		plt.ylabel('Gravimetric Capacitance F/g')
		plt.title('Capacitance against cycle number')
		#plt.savefig(input('What do you want to save the Capacitance against cycle number graph as? Do not forget to add .png at the end '), dpi=300)
		plt.show()

		#plots ESR plot against cycle number
		plt.plot(cycle_numbers,ESR_values)
		plt.title('ESR against cyclenumber in Ω')
		#plt.savefig(input('What do you want to save the ESR against cycle number graph as? Do not forget to add .png at the end '), dpi=300)
		plt.show()

		#plots capacity against cycle number
		plt.plot(cycle_numbers,capacity_values)
		plt.title('Capacity against cyclenumber')
		#plt.savefig(input('What do you want to save the Capacity against cycle number graph as? Do not forget to add .png at the end '), dpi=300)
		plt.show()

		#plots Full capacitance against cycle number
		plt.plot(cycle_numbers,fullcapacitance_values)
		plt.title('Full discharge Capacitance against cyclenumber')
		plt.xlabel('Cycle number')
		plt.ylabel('Capacitance (F/g)')
		plt.show()

		print('mean capacitance across all cycles is ',np.mean(capacitance_values))
		print('mean IR drop across all cycles is ', np.mean(IRdrop_values), ' and the mean ESR is ', np.mean(ESR_values))
		print('mean Capacity across all cycles is ',np.mean(capacity_values))


	def getcapacitance(self):

		import numpy as np            #necessary initialisation stuff
		import matplotlib.pyplot as plt
		from scipy.stats import linregress
		pathway=input('what is the pathway? (when you upload the file, right click and copy path) ')
		currentdensity=input('what is the current density in A/g? ')
		currentdensity=float(currentdensity)
		current=float(input('what is the mass of the electrode in mg? '))*currentdensity*0.001
		cycles=int(input('How many cycles have you inputted? '))
		peakvoltage=float(input('what is the peak voltage? e.g. O.8V 1.0V? '))
		steps=int(input('How many steps in the gradient would you like to take? '))


		time= self.data['time/s']
		voltage = self.data['Ewe/V']
		uneditedtime=time       #the time array will be edited and cut off along the way in the code. Unedited time will stay the same.
		uneditedvoltage=voltage   #the voltage array will be edited and cut off along the way in the code. Unedited voltage will stay the same.
		size=np.prod(time.shape) #size of the array, will be used later on a lot (how many data points)
		dVdt= []
		#need to now differentiate between vertical and diagonal line
		#use derivatives
		#use a loop
		for j in np.arange(1,size//steps, 1): #calculates gradient every 'steps' number of points
		  derivative=(voltage[steps*j]-voltage[steps*(j-1)])/(time[steps*j]-time[steps*(j-1)])
		  dVdt.append(derivative)
		#the loop above works out the derivative between every 'steps' points and adds it to an array called dVdt which stores all the gradients
		plt.plot(time,voltage)
		plt.xlabel('Time/s')
		plt.ylabel('Voltage/V')
		plt.title('GCD you inputted') #plots the GCD
		plt.show()
		lengthofdVdt=len(dVdt)
		remainder= np.prod(time.shape) % steps #let's say you take every 5 points but you have 7 points overall. This removes the last 2 points temporarily so that the gradient can be plotted
		if remainder>0:
		    remaindertime=time[:-remainder]
		else:
		    remaindertime=time
		gradtime=remaindertime[::steps]
		plt.plot(gradtime[:-1],dVdt)
		plt.xlabel('Time/s')
		plt.ylabel('Rate of change of Voltage/Vs\u207b\u00b9 ')
		plt.title('dVdt graph for whole GCD')     #plots the gradient function over the whole GCD
		plt.show()
		dischargev = {}   #messy array stuff.. dischargev,t,dVdt stores the full discharge curve for every cycle. Verticalv,t,dVdt stores every vertical section for every cycle
		discharget = {}   #diagonalv,t,dVdt stores every diagonal section for every cycle (voltage, time and rate of change in voltage(dV/dt))
		dischargedVdt = {}
		verticaldVdt = {}
		verticalt = {}
		verticalv= {}
		diagonaldVdt = {}
		diagonalt = {}
		diagonalv= {}
		capacity = {}   #will store capacity for every cycle number
		capacitance= {} #stores Capacitance for every cycle number
		fullcapacitance= {}
		IRdrop= {}
		ESR = {}
		endofcycle=0
		for cyclenumber in np.arange(0, cycles, 1): #repeats for every cycle
		    dVdt = dVdt[endofcycle:]    #removes the previous cycle it analysed from the data that is yet to be analysed, effectively moving on to analyse the next cycle
		    time = time[steps * endofcycle:]
		    voltage = voltage[steps * endofcycle:]
		    investigate = dVdt[:lengthofdVdt // (cycles + 1)] #needs to find the initial vertical drop. Which corresponds to the minimum in gradient. However that's only within the cycle.
		    # So we have to make it such that it only takes the data from the cycle it is analysing. Let's say there are 4 cycles, we know that in the first 1/5 of the total data, the 
		    # first minima will be in there. when it repeats, it removes the first cycle. so now it tests the second cycle... etc

		    beginningofdischarge = np.argmin(investigate)      #removes any charging and a bit of the voltage drop, makes it easier to find the end of the voltage drop

		    voltage = voltage[steps * (beginningofdischarge):] #edits the voltage to remove the charging part and keep only the discharge part
		    time = time[steps * (beginningofdischarge):]
		    dVdt = dVdt[beginningofdischarge:]

		    for endofcycle, loop in enumerate(dVdt):  # removes any of the charging part that may come after the diagonal line
		        if endofcycle >= (len(dVdt)-1) or loop > 0.00:
		            dischargev[cyclenumber] = voltage[:steps * (endofcycle)]  #removes charging part from the array
		            discharget[cyclenumber] = time[:steps * (endofcycle)]
		            dischargedVdt[cyclenumber] = dVdt[:endofcycle]
		            break
		    temporaryv = dischargev[cyclenumber]  #temporaryv,t,dVdt are needed because the dischargev,t,dVdt are dictionaries. Think of them as a table made of rows and columns and each 
		    #column corresponds to the dischargev,t,dVdt for each cycle. To edit the values in the column, we need an array because we use array cutting methods throughout this analysis
		    #whenever we use something like voltage=voltage[:something] this is cropping an array. So we take each column in the dict and make it an array and then edit that array. Then
		    #equal that array back to the column in the dict.
		    temporaryt = discharget[cyclenumber]
		    temporarydVdt = dischargedVdt[cyclenumber]


		    #METHOD OF FINDING IR DROP
		    #Current method used is to take the gradient of the full discharge section and find it's mean.
		    # We see a spike that corresponds to the Ir drop and a relatively flat, horizontal line which corresponds to the diagonal section.
		    # The mean will be effectively the y value of the flat line and sp when the gradient first goes to this value, we consider any subsequent data as the diagonal section 
		    # and any section before it as the vertical, IR drop, part.
		    threshold = np.mean(temporarydVdt) #mean of gradient of discharge part
		    for i1, loop in enumerate(temporarydVdt): #finds the end of the voltage drop by finding when the gradient goes above the mean
		        if 0 > loop > threshold:
		            endofIRdrop = i1 #endofIRdrop becomes the index corresponding to what position in the dVdt array it is when it goes above the mean
		            break
		    verticaldVdt[cyclenumber] = temporarydVdt[:endofIRdrop] #removes any discharge part that's associated with the diagonal section so only the vertical section remains
		    verticalt[cyclenumber] = temporaryt[:steps * endofIRdrop]
		    verticalv[cyclenumber]= temporaryv[:steps * endofIRdrop]
		    diagonaldVdt[cyclenumber] = temporarydVdt[endofIRdrop:] #removes any discharge part that's associated with the vertical section so only the diagonal section remains
		    diagonalt[cyclenumber] = temporaryt[steps * endofIRdrop:]
		    diagonalv[cyclenumber] = temporaryv[steps * endofIRdrop:]
		    temporaryt=diagonalt[cyclenumber] #The diagonal section needs to be analysed when working out capacity. We need to make the time and voltage values associated with the cycle
		    #into an array so we can take the last and first value out. We can't do this with diagonalt as it's a dict not an array. Imagine it as a book, chapters and pages:
		    #you can only state the book and what chapter it is (dict and what column) and not the page as well. However making it an array basically keeps only the chapter 
		    #and then you can state which page in the chapter it is in. 
		    slope, intercept, _, _, _ = linregress(diagonalt[cyclenumber], diagonalv[cyclenumber]) #works out slope of discharge and therefore the capacitance
		    capacitance[cyclenumber]= -2 * currentdensity / slope #equation cancels out the masses: assumes both electrodes have the same mass. then since m1+m2=2*m1=2*m2 then (m1+m2)/m is 2


		capacitance_values = list(capacitance.values())
		return capacitance_values
		
