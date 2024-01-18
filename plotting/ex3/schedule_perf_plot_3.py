import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from datetime import datetime

# TODO: set file names manually
MCPERF_FILE = 'memc_3.csv'
PODS_FILE = 'times_3.csv'

def load_mcperf_data():
    ''' 
        returns: vectors of latency and start times of mcperf
    '''
    # x_vals: 95th percentile (tail latency), y_vals: actual QPS
    data_mat = np.empty((19, 0))
    filename = MCPERF_FILE
    run_i = np.loadtxt(filename, delimiter=',')
    data_mat = np.append(data_mat, run_i, axis=1)

    # convert ms to s
    p_95 = data_mat[:, 0] / 1000
    # TODO: do we need QPS data for plot?
    QPS = data_mat[:, 1]
    ts_start = data_mat[:, 2]
    ts_end = data_mat[:, 3]

    return p_95, ts_start, ts_end


def load_pods_data():
    '''
        returns: lists of jobs, start times and execution times
    '''
    filename = PODS_FILE
    # read from .csv file
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    jobs, t_start, t_exec = [], [], []
    # not taking the memcached data here (change index to fo from 1 to 9)
    for i in range(1, 8):
        jobs.append(data[i][0])
        t_exec.append(int(data[i][2]))
        t_s = datetime.strptime((data[i][1])[1:], '%H:%M:%S').time()
        t_s_sec = t_s.second + t_s.minute * 60 + t_s.hour * 3600
        t_start.append(t_s_sec)
        
    return jobs, t_start, t_exec


def format_plot(fig_ax):
    '''
        format bar chart (mcperf) as specified in task description.
    '''
    # axes
    fig_ax.set_xlabel("Time [s]")
    fig_ax.set_ylabel("$\mathregular{95^{th}}$ percentile latency [ms]", rotation=0)
    fig_ax.yaxis.set_label_coords(0.001, 1.02)
    fig_ax.set_xlim(-5, 230)
    fig_ax.set_ylim(0, 1.2)
    fig_ax.set_xticks(np.arange(0, 230, 10), labels=None, minor=True)
    fig_ax.set_xticks(np.arange(0, 240, 20), labels=["0", "20s", "40s", "60s", "80s", "100s", "120s", "140s", "160s", "180s", "200s", "220s"])

    # grid and background
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.set_axisbelow(True)
    fig_ax.grid(axis='x', color='white', linewidth=1.0)



def format_schedule_plot(fig_ax):
    '''
        format schdule bar chart.
    '''
    # TODO: set run nr. manually
    fig_ax.set_title("Run 3: PARSEC scheduling policy and $\mathregular{95^{th}}$ percentile latency of memcached", loc='left', pad=40)

    fig_ax.set_xlim(-5, 230)
    fig_ax.set_ylim(0, 4)
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.set_axisbelow(True)
    fig_ax.grid(axis='x', color='white', linewidth=1.0)

    # set x labels
    fig_ax.set_xticks(np.arange(0, 230, 10), labels=None, minor=True)
    fig_ax.set_xticks(np.arange(0, 240, 20), labels=["0", "20s", "40s", "60s", "80s", "100s", "120s", "140s", "160s", "180s", "200s", "220s"])

    # set y labels
    fig_ax.set_yticks([1, 2.25, 3.25], labels=["node-c-8core", "node-b-4core", "node-a-2core"])




def main():

    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10, 7))

    # #---------------------------------------schedule-----------------------------------------
    # jobs and colors
    job_names = ['blackscholes', 'canneal', 'dedup', 'ferret', 'freqmine', 'radix', 'vips', 'memcached']
    colors = ['goldenrod', 'palegoldenrod', 'thistle', 'lightblue', 'limegreen', 'mediumturquoise', 'firebrick', 'darkkhaki']
    # c = 1, b = 3
    y_val = [2, 0.5, 1, 2, 1, 2, 0.5, 3]

    # create plot
    format_schedule_plot(ax[0])

    jobs, t_start, t_exec = load_pods_data()
    print(jobs)
    t_start = np.array(t_start)
    t_exec = np.array(t_exec)

    # normalize start times
    t_start_norm = (t_start - min(t_start))
    t_end_norm = t_start_norm + t_exec

    # append memcached
    t_start_norm = np.append(t_start_norm, 0)
    t_end_norm = np.append(t_end_norm, max(t_end_norm))

    #plot horizontal bars
    for i in range(len(t_start_norm)):
        rects = ax[0].barh(y_val[i], width=t_end_norm[i]-t_start_norm[i], height=0.5, left=t_start_norm[i], align='edge', color=colors[i], alpha=1, label=job_names[i])
        ax[0].bar_label(rects, label_type='center', color='black')

    # legend
    ax[0].legend(ncol=len(job_names), bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')
    #----------------------------------------------------------------------------------------

    #---------------------------------------bar chart memcached ---------------------------------------
    format_plot(ax[1])

    # load and process data
    p_95, ts_start, ts_end = load_mcperf_data()
    delta = (ts_end - ts_start) / 1000
    begin_memcached = ts_start[0]
    ts_start = (ts_start - begin_memcached) / 1000

    # SLO line
    x_slo = np.linspace(-5, 230, 100)
    y_slo = np.ones(100)

    # plot
    ax[1].bar(ts_start, p_95, width=delta, align='edge', color='dimgrey', alpha=1)
    ax[1].plot(x_slo, y_slo, color='red', linestyle='--', linewidth=1.0, label="SLO")

    # legend
    ax[1].legend()

    plt.tight_layout()

    # TODO: set file name manually
    plt.savefig("plot_3_3.pdf")
    #----------------------------------------------------------------------------------------



    return


if __name__ == "__main__":
    main()