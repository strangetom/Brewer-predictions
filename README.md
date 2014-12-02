#####Authors
James Glackin james.glackin@student.manchester.ac.uk  
Thomas Strange thomas.strange-2@student.manchester.ac.uk
____ 
#####About

BrewerPredict.exe reads the last 10 data points from standard lamp log files (SLOAVG.nnn) created by the Brewer. It applies a quadratic polynomial fit to these data points in order to make a prediction of the next two, and outputs these values to the console and a text file (Prediction.txt).  
Predictions can be made with less than 10 data points but accuracy of the prediction will be limited. BrewerPredict.exe will not make a prediction with less than 4 data points, as the polynomial fit will have more parameters than data points, making the predictions unrealiable.  

Icon from http://www.iconsdb.com/orange-icons/beer-icon.html  
The code is written in Python 2.7.6 and compiled using Pyinstaller 2.1. 

____ 
#####Usage

Place executable and standard lamp log file for the Brewer in the same folder. 
Double click the executable to run, and follow on screen prompts.  
