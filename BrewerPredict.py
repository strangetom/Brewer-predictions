###########################################################################################################
# Brewer R6 next day prediction.                                                                                                                      #
#                                                                                                         #          
#TS JG 11-2014                                                                                              #
###########################################################################################################
import numpy as np
import sys

filename = raw_input('Enter file containing at least 10 previous readings\n>> ')

try:
	#Load data
	data = np.genfromtxt(filename,delimiter=(5, 3, 3, 3, 6, 6, 6, 6, 6, 6, 8, 3, 3, 3, 3, 3, 3, 6),autostrip=True)
	#Remove any rows containing NaN
	data = data[~np.isnan(data).any(1)]
except IOError:
	print "Error: File cannot be found in current directory."
	raw_input("\nPress any key to exit.")
	sys.exit()

#Extract last 10 R6 values
R6=data[:,9][-10:]
if R6.shape[0] < 4:
	print "Insufficicent number of data points to predict from."
	raw_input("\nPress any key to exit.")
	sys.exit()
elif R6.shape[0] < 10:
	print "Too few data point. Prediction may not be accurate."
	fit_params = np.polyfit(np.arange(1,R6.shape[0]+1,1),R6,2)
else: 
	fit_params = np.polyfit(np.arange(1,11,1),R6,2)

#Calculate fitted values
fity = np.polyval(fit_params,np.arange(1,13,1))
    
#Return data on N+1,N=2 predictions. 
predicted_R6_1 = fity[-2]
predicted_R6_2 = fity[-1]

print "Next:	 {:.4f}".format(predicted_R6_1)
print "Next +1: {:.4f}".format(predicted_R6_2)

f = open('Predictions.txt', 'w')
f.write('Next data point prediction =  {:.4f}\n'.format(predicted_R6_1))
f.write('Next data point +1 prediction = {:.4f}'.format(predicted_R6_2))
f.close()

raw_input("\nPress any key to exit.")


