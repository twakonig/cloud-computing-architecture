import numpy as np
import csv

filename = 'meas_real_2a.csv'

array = []
with open(filename, 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        array.append(row)

# convert to value in seconds and create numpy array
rows = len(array)
cols = len(array[0])
data_mat = np.empty((rows, cols))

for i in range(rows):
    row_i = []
    for j in range(cols):
        val_str = array[i][j].strip()
        row_i.append(60 * int(val_str[0]) + float(val_str[2:7]))
 
    data_mat[i, :] = row_i

# create runtime output
runtime_mat = data_mat
print('Runtime in seconds:')
print(runtime_mat)
jobs = ["blackscholes", "canneal", "dedup", "ferret", "freqmine", "radix", "vips"]
# write runtime into .csv file "runtime_seconds.csv"
np.savetxt('runtime_seconds.csv', runtime_mat, delimiter=',', fmt='%1.3f')



# numpy divide data_mat by first column (normalized execution time)
data_mat = data_mat / data_mat[:, 0].reshape(-1, 1)
data_mat = np.round(data_mat, 2)
print(data_mat)