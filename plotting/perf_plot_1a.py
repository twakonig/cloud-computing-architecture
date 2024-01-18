import numpy as np
import matplotlib.pyplot as plt
import os


def load_data(config):
    ''' 
        load data of all three runs of given config 
        (y_vals given in [mikro_s], hence / 1000)
        returns: matrix of x_vals (17x3), matrix of y_vals (17x3)
    '''
    # x_vals: 95th percentile (tail latency), y_vals: actual QPS
    data_mat = np.empty((17, 0))
    for i in range(3):
        filename = 'meas_p95_QPS_' + config + '_' + str(i+1) + '.csv'
        run_i = np.loadtxt(filename, delimiter=',')
        data_mat = np.append(data_mat, run_i, axis=1)

    y_vals = data_mat[:,[0,2,4]]
    x_vals = data_mat[:,[1,3,5]]

    return x_vals, y_vals / 1000


def format_plot(fig_ax):
    '''
        format plot as specified in task description.
    '''
    # axes
    fig_ax.set_xlabel("Queries per second (QPS)")
    fig_ax.set_ylabel("$\mathregular{95^{th}}$ percentile latency [ms]", rotation=0)
    fig_ax.yaxis.set_label_coords(0.001, 1.02)
    fig_ax.set_xlim(0, 110000)
    fig_ax.set_ylim(0, 8)
    fig_ax.set_xticks(np.arange(0, 110000, 5000), labels=None, minor=True)
    fig_ax.set_xticks(np.arange(0, 110000, 10000), labels=["0", "10K", "20K", "30K", "40K", "50K", "60K", "70K", "80K", "90K", "100K"])

    # grid and background
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.grid(axis='y', color='white', linewidth=1.0)
    fig_ax.grid(which='both', axis='x', color='white', linewidth=1.0)

    # title
    fig_ax.set_title("Impact of hardware resource interferences on tail latency of 'memchached' application", loc='left', pad=40)



def main():

    # create plot
    fig = plt.figure(figsize=(9, 7))
    fig_ax = fig.gca()
    format_plot(fig_ax)
    colors = ['red', 'mediumblue', 'darkorchid', 'goldenrod', 'forestgreen', 'darkorange', 'cadetblue']
    interferences = ["none", "cpu", "l1d", "l1i", "l2", "llc", "membw"]
    markers = ['o', 'h', 'D', 'v', '8', 's', 'd']

    # change directory to read data files
    os.chdir('../results/1')

    # load and plot data
    for i in range(len(interferences)):
        x_vals, y_vals = load_data(interferences[i])
        x_mean = np.mean(x_vals, axis=1)
        y_mean = np.mean(y_vals, axis=1)

        # choose error measure (std deviation or 95th percentile)
        x_err = np.std(x_vals, axis=1)
        y_err = np.std(y_vals, axis=1)
        # x_err = np.percentile(x_vals, 95, axis=1) - x_mean
        # y_err = np.percentile(y_vals, 95, axis=1) - y_mean
        
        # post-processing to reduce cluttering on plot
        for j in range(1, len(x_mean)):
            # cut all arrays associated with that line to same length
            if((x_mean[j] - x_mean[j-1]) < 1000):
                x_mean = x_mean[0:j]
                y_mean = y_mean[0:j]
                x_err = x_err[0:j]
                y_err = y_err[0:j]
                break

        fig_ax.errorbar(x_mean, y_mean, xerr=x_err, yerr=y_err, ecolor=colors[i], elinewidth=0.6, barsabove=False, capsize=2, capthick=1, fmt='none', mec='white', mew=0.4, alpha=0.8)
        fig_ax.plot(x_mean, y_mean, marker=markers[i], mec='white', mew=0.7, ms=4.5, c=colors[i], linewidth=1.2, label=interferences[i], alpha=0.8)
        print(interferences[i], ' num_points used: ', len(x_mean))

    fig_ax.legend(title='Interference types: ', loc='upper right')
    
    # change directory to store plot
    os.chdir('../../plotting/plots/1')
    plt.tight_layout()
    plt.savefig("plot_1a.pdf")

    return


if __name__ == "__main__":
    main()