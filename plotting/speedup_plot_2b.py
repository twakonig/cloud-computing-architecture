import numpy as np
import csv
import matplotlib.pyplot as plt
import os

def get_data(filename):
    # read data from csv file
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
            row_i.append(60 * int(val_str[0]) + round(float(val_str[2:7]), 2))
    
        data_mat[i, :] = row_i

    # get runtime per number of threads
    print(data_mat)
    # write to "runtime_seconds_t_1_2_4_8.csv" file
    np.savetxt('runtime_seconds_t_1_2_4_8.csv', data_mat, delimiter=',', fmt='%1.3f')
            
    # get speedup
    speedup_mat = data_mat[:, 0].reshape(-1, 1) / data_mat[:, 1:]
    speedup_mat = np.round(speedup_mat, 2)
    speedup_mat = np.insert(speedup_mat, 0, 1, axis=1)

    return speedup_mat


def format_plot(fig_ax):
    '''
        format plot as specified in task description.
    '''
    # axes
    fig_ax.set_xlabel("Number of threads")
    fig_ax.set_ylabel("Speedup", rotation=0)
    fig_ax.yaxis.set_label_coords(0.001, 1.02)
    fig_ax.set_xlim(0, 9)
    fig_ax.set_ylim(0, 7)
    fig_ax.set_xticks(np.arange(0, 9, 1), labels=None, minor=True)
    fig_ax.set_xticks([1, 2, 4, 8], labels=["1", "2", "4", "8"], minor=False)

    # grid and background
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.grid(axis='y', color='white', linewidth=1.0)
    fig_ax.grid(which='both', axis='x', color='white', linewidth=1.0)

    # title
    fig_ax.set_title("Speedup of batch applications with increasing number of threads", loc='left', pad=40)



def main():
    filename = 'meas_real_2b.csv'

    speedup_mat = get_data(filename)

    fig = plt.figure(figsize=(10, 8.6))
    fig_ax = fig.gca()
    format_plot(fig_ax)
    colors = ['red', 'mediumblue', 'darkorchid', 'goldenrod', 'forestgreen', 'darkorange', 'cadetblue']
    jobs = ["blackscholes", "canneal", "dedup", "ferret", "freqmine", "radix", "vips"]
    markers = ['o', 'h', 'D', 'v', '8', 's', 'd']

    # plot speedup
    x_vals = np.array([1, 2, 4, 8])
    for i in range(7):
        y_vals = speedup_mat[i, :]
        fig_ax.plot(x_vals, y_vals, color=colors[i], marker=markers[i], mec='white', mew=0.7, ms=7, label=jobs[i], alpha=0.8)

    fig_ax.legend(loc='upper left', bbox_to_anchor=(0.01, 0.99), fancybox=False, shadow=False, title="Applications: ")

    # change directory to store plot
    os.chdir('plots/2b')
    plt.tight_layout()
    plt.savefig("plot_2b.pdf")


if __name__ == '__main__':
    main()