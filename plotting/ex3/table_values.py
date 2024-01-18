import numpy as np
import csv


def load_pods_data():
    '''
        returns: lists of jobs, start times and execution times
    '''
    exec_t_mat = []
    files = ['times_1.csv', 'times_2.csv', 'times_3.csv']
    for i in range(3):
        filename = files[i]
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        exec_t = []
        for j in range(1, 9):
            exec_t.append(int(data[j][2]))
        exec_t_mat.append(exec_t)

    return exec_t_mat


def main():
    data_mat = load_pods_data()
    t_exec = np.array(data_mat)
    mean_time = np.mean(t_exec, axis=0)
    std_dev = np.std(t_exec, axis=0)

    # results for table 3.1)
    print('mean time: ', np.round(mean_time, 2))
    print('std dev: ', np.round(std_dev,2 ))

if __name__ == '__main__':
    main()