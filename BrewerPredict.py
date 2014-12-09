""" 
Created on 09-12-2014.

@author: James Glackin, Tom Strange. 

Predicts the next two R6 values and estimates error from Brewer standard lamp data.
Calculates the avergae standard deviation of the fit applied to predict the next two R6 values.
Plots relevant data that may be needed.
Saves plots in .png format.
Saves data in .txt files.  
Icon from http://www.iconsdb.com/orange-icons/beer-icon.html

"""

import numpy as np 
import matplotlib.pyplot as plt
import sys

def stand_dev(value, pred_1, pred_2):
    
    #Calculate standard dev. of next value predictions.  
    diff = value[11:] - pred_1[:-1]
    summation = np.sum(diff**2,axis = 0) 
    dev = np.sqrt(summation/len(pred_1))

    #Calculate standard dev. of next +1 value predictions. 
    diff2 = value[12:] - pred_2[:-2]
    summation2 = np.sum(diff2**2,axis = 0) 
    dev2 = np.sqrt(summation2/len(pred_2))

    return dev, dev2

def data_fit(R6):
    #Initialise variables. 
    predicted_R6_1 = np.zeros(shape=(R6.shape[0]-10,))
    predicted_R6_2 = np.zeros(shape=(R6.shape[0]-10,))
    #R6.shape[0]-10 is the size of the predicted arrays because we use the first
    #10 values of R6 to predicted the 11th.

    for i in range(10, R6.shape[0]):
        #Set indices 
        idx_min = i-10
        idx_max = i
    
        #Cut down data for fitting
        R6_cut = R6[idx_min:idx_max]
        fitx_1 = np.arange(1,11,1)
        fitx_2 = np.arange(1,13,1)
    
        #Fitting data 
        fit_params = np.polyfit(fitx_1,R6_cut,2)
        fity = np.polyval(fit_params,fitx_2)
    
        #Return data on N+1,N=2 predictions. 
        predicted_R6_1[i-10] = fity[-2]
        predicted_R6_2[i-10] = fity[-1]
    
    return predicted_R6_1, predicted_R6_2

valid_name = False
while valid_name == False:
        
    filename = raw_input('Enter filename (sloavg.nnn) of data. Data must have more than 10 data points in order to give accurate results\n>> ')
    try:
        #Load data
        data = np.genfromtxt(filename,delimiter=(5, 3, 3, 3, 6, 6, 6, 6, 6, 6, 8, 3, 3, 3, 3, 3, 3, 6),autostrip=True)
        #Remove any rows containing NaN
        data = data[~np.isnan(data).any(1)]
        R6 = data[:,9]
        day = np.arange(1,R6.shape[0]+1,1)
        valid_name = True
    except IOError:
        print "Error: File cannot be found in current directory."

while True:

    print "What would you like to do? \n"
    print "[1] Predict the next 2 R6 values."
    print "[2] Calculate the standard deviation of the fit (without a scatter plot of actual data vs. prediction)."
    print "[3] Calculate the standard deviation of the fit (with a scatter plot of actual data vs. prediction)."
    print "[4] Plot the actual and predicted R6 values for comparison."
    print "[0] Exit."

    valid_choices = [0, 1, 2, 3, 4]
    loop = True
    while loop:
        try:
            decide = int(raw_input("\nEnter the number of your choice and press enter to continue \n>> "))
            if decide in valid_choices:
                loop = False
        except ValueError:
            print "Not a valid input. Please enter [0],[1],[2],[3] or [4] \n."

    if decide == 1:

        R6_new = R6[-10:]
        R6_sd_new = data[:,16][-10:]
        if R6_new.shape[0] < 4:
            print "Insufficicent number of data points to predict from."
            raw_input("\nPress any key to exit.")
            sys.exit()
        elif R6_new.shape[0] < 10:
            print "Too few data point. Prediction may not be accurate."
            fit_params = np.polyfit(np.arange(1,R6_new.shape[0]+1,1),R6,2)
        else: 
            fit_params = np.polyfit(np.arange(1,11,1),R6_new,2)

        #Calculate fitted values
        fity = np.polyval(fit_params,np.arange(1,13,1))

        #Calculate average fractional standard deviation
        mean_sd = np.mean(R6_sd_new/R6_new)
            
        #Return data on N+1,N=2 predictions. 
        predicted_R6_1_new = fity[-2]
        predicted_R6_1_sd_new = predicted_R6_1_new*mean_sd
        predicted_R6_2_new = fity[-1]
        predicted_R6_2_sd_new = predicted_R6_2_new*mean_sd

        #Output file
        savename = filename + '_prediction.txt'
        with open(savename, 'w') as f:
            f.write('Predicted value \t Error on predicted value\n')
            f.write('{:.2f} \t {:.2f}\n'.format(predicted_R6_1_new,predicted_R6_1_sd_new))
            f.write('{:.2f} \t {:.2f}'.format(predicted_R6_2_new,predicted_R6_2_sd_new))

    if decide == 2:    
        
        predicted_R6_1, predicted_R6_2 = data_fit(R6)
        dev, dev2 = stand_dev(R6,predicted_R6_1,predicted_R6_2)    
        
        #Write standard devs. to text file.
        savename = filename + '_standard_dev.txt'
        with open(savename, 'w') as f:
            f.write('Average standard deviation\n')
            f.write('{:.2f}\n'.format(dev))
            f.write('{:.2f}'.format(dev2))
        
    elif decide == 3:
        
        predicted_R6_1, predicted_R6_2 = data_fit(R6)
        dev, dev2 = stand_dev(R6,predicted_R6_1,predicted_R6_2)        
         
        #Write standard devs. to text file. 
        savename = filename + '_standard_dev.txt'
        with open(savename, 'w') as f:
            f.write('Average standard deviation\n')
            f.write('{:.2f}\n'.format(dev))
            f.write('{:.2f}'.format(dev2))
        
        #PLot the scatter of the actual value vs. the prediction, with line y=x for comparison. 
        fig, axes = plt.subplots(2, 1, figsize=(8,8))
        axes[0].scatter(R6[11:],predicted_R6_1[:-1],color='r',s=3)
        axes[0].set_ylabel('Predicted R6 (Next Value)')
        axes[0].hold(True)
        axes[0].set_title('Actual R6 vs. Predicted Next R6 Scatter Plot') 
        axes[0].plot(R6[11:],R6[11:],'k')
        
        axes[1].scatter(R6[12:],predicted_R6_2[:-2],color='b',s=3) 
        axes[1].set_xlabel('Measured R6')
        axes[1].set_ylabel('Predicted R6 (Next Value +1)')
        axes[1].hold(True)
        axes[1].set_title('Actual R6 vs. Predicted Next +1 R6 Scatter Plot') 
        axes[1].plot(R6[12:],R6[12:],'k')
        
        
        savename = filename + '_scatterplot.png'
        fig.savefig(savename)
        plt.close("all")


    elif decide == 4:

        predicted_R6_1, predicted_R6_2, = data_fit(R6)
        
        #Plot N+1 Graphs and save. 
        fig, axes = plt.subplots(2, 1, figsize=(16,8))
        axes[0].plot(day,R6,'b',label='Actual Value') 
        axes[0].set_ylabel('R6 Value')
        axes[0].hold(True)
        axes[0].set_title('Next predicted and actual R6 Value') 
        axes[0].plot(day[11:],predicted_R6_1[:-1],'r',linewidth=0.6,label = 'Next Predicted Value')
        axes[0].legend()

        axes[1].plot(day,R6,'b',label='Actual Value') 
        axes[1].set_xlabel('Measurement Number')
        axes[1].set_ylabel('R6 Value')
        axes[1].hold(True)
        axes[1].set_title('Next +1 predicted and actual R6 Value') 
        axes[1].plot(day[12:],predicted_R6_2[:-2],'r',linewidth=0.6,label = 'Next +1 Predicted Value')
        axes[1].legend()

        savename = filename + '_fitplot.png'
        fig.savefig(savename)
        plt.close("all")

    elif decide == 0:
        sys.exit()
     
    elif decide > 4:
        print "Invalid Input. Please enter either [0],[1],[2], [3] or [4] according to the above instructions"
