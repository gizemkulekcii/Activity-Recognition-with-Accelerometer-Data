
import csv
import matplotlib.pyplot as plt
import math
from scipy import signal
import scipy.signal 

rows = [] 

#taking the filename as input 
csv_filename = input( "Please enter the filename : ")

#reading the csv file and adding rows to the list named rows line by line
with open(csv_filename, 'r' ) as file:
    data= csv.reader(file)
    header= next(data) # next method: returns the current row and moves to next row
    for row in data:
        rows.append(row) 
       
       
time = []
acc = []

#finding acceleration and adding it to the list named acc
for i in range(0, len(rows)):
   row = rows[i][0].split(";")
   if i == 0:
       t= float(row[1])
   time.append((float(row[1])-t)) 
   a = math.sqrt((pow(float(row[3]),2)+pow(float(row[4]),2)+pow(float(row[5]),2)))
   acc.append(a)

acc_detrend = signal.detrend(acc)

#Low-pass Filter

sample_rate = int(len(time)/(time[len(time)-1]-time[0]))
sample_period = time[len(time)-1]-time[0]
total_sample = sample_rate * sample_period
nyquist_freq = 0.5 * sample_rate
cutoff = 3
normal_cutoff = cutoff / nyquist_freq

b, a = scipy.signal.butter(4, normal_cutoff, btype='lowpass', analog=False)
y_axis = scipy.signal.filtfilt(b ,a ,acc_detrend )

#computing step count from the data using sliding window and peak detection

#finding the moving mean(series of averages of different subsets of the data set) using sliding window technique

moving_mean = []
window_size = 5
window = y_axis[0:window_size]
window_sum = sum(window)
mean =  window_sum / window_size
moving_mean.append(mean)

i= 1
while i < len(y_axis)-window_size +1 :
    window = y_axis[i:i+window_size]
    window_sum = sum(window)
    mean = window_sum / window_size
    moving_mean.append(mean)
    i += 1

#peak detection 

step_counter = 0
threshold = 0.02 #threshold value
min_height_of_peaks = sum(moving_mean) / len(moving_mean)

if moving_mean[0] >= moving_mean[1] and moving_mean[0] > min_height_of_peaks and moving_mean[0] > threshold:
    step_counter += 1
    
if moving_mean[len(moving_mean)-1] >= moving_mean[len(moving_mean)-1] and moving_mean[len(moving_mean)-1] > min_height_of_peaks and moving_mean[len(moving_mean)-1]  > threshold:
    step_counter += 1

for i in range(1, len(moving_mean)-1):
    if moving_mean[i] > min_height_of_peaks and moving_mean[i] >= moving_mean[i-1] and moving_mean[i] >= moving_mean[i+1] and  moving_mean[i] > threshold:
        step_counter += 1


print( str(step_counter) + ' steps taken in ' + str( int(time[len(time)-1]) ) + ' seconds')

#plotting the data
plt.plot(time ,y_axis)
plt.show()
