#####Authors
James Glackin james.glackin@student.manchester.ac.uk  
Thomas Strange thomas.strange-2@student.manchester.ac.uk
____ 
#####About

BrewerPredict.exe reads the last 10 data points from standard lamp log files (SLOAVG.nnn) created by the Brewer. It applies a polynomial fit to these data points, in order to make a prediction of the next two, outputting these values to the console and to a .txt files (Prediction.txt). Predictions can be made with less than 10 data points but accuracy of the prediction will be limited. BrewerPredict.exe will not make a prediction with less than 4 data points, as the polynomial fit will have more parameters than data points, making the predictions unrealiable.  

The code is written in Python 2.7.6 and compiled using Pyinstaller 2.1. 

____ 
#####Usage

Place execitable in your desired folder, along with the standard lamp log file for the brewer you want to predict the R6 values for. 
Double click to run, and follow on screen prompts.  