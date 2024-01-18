import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from datetime import datetime
import fill_table
from matplotlib.patches import Patch

directory = "data/"
# TODO: manually set the run R
R = 3

def load_mcperf_data():
    ''' 
        returns: vectors of latency and start times of mcperf
    '''
    data_files = ["4_3_p95_QPS_1.csv", "4_3_p95_QPS_2.csv", "4_3_p95_QPS_3.csv"]
    lantecies_all = []
    qps_all = []

    for d in data_files:
        latencies = []
        qps = []
        filename = directory + d

        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                # do something
                data = line.split(', ')
                latencies.append(round((float(data[0]) / 1000), 2))
                qps.append(float(data[1].split('\n')[0]))
                # read next line
                line = f.readline()

        lantecies_all.append(latencies)
        qps_all.append(qps)

    # declare numpy arrays and trasnpose (1 column per run, 100 rows for time intervals) (100x3 matrices)
    lantecies_all = np.array(lantecies_all)
    lantecies_all = np.transpose(lantecies_all)
    qps_all = np.array(qps_all)
    qps_all = np.transpose(qps_all)

    return lantecies_all, qps_all


def load_cpu_jumps(run):
    '''
        returns: x and y values for jumps in cpu usage
    '''
    filename = directory + "memcached_jumps_" + str(run+1) + ".txt"
    x_jumps = []
    y_jumps = []

    with open(filename, 'r') as f:
        ts_single = f.readline().split(', ')[:-1]
        ts_double = f.readline().split(', ')[:-1]

    for i in range(len(ts_single)):  
        t = ts_single[i].split(':')
        t = 3600 * int(t[0]) + 60 * int(t[1]) + float(t[2])
        ts_single[i] = round(t, 2)

    for i in range(len(ts_double)):  
        t = ts_double[i].split(':')
        t = 3600 * int(t[0]) + 60 * int(t[1]) + float(t[2])
        ts_double[i] = round(t, 2)

    for j in range(len(ts_single) + len(ts_double)):
        if j % 2 == 0:
            x_jumps.append(ts_single[int(j/2)])
            y_jumps.append(1)
        else:
            x_jumps.append(ts_double[int((j-1)/2)])
            y_jumps.append(2)

    x_jumps = np.array(x_jumps)
    y_jumps = np.array(y_jumps)

    return x_jumps, y_jumps


def load_cat1_data(job):
    '''
        returns: lists of jobs, start times and execution times
        ONLY CAT1 JOBS
    '''
    # load data of all parsec jobs: vectors of timestamps for pause and unpause in seconds
    # pause and unpause only for cat1 jobs
    # pause_logs = ["pause_log1.txt", "pause_log2.txt", "pause_log3.txt"]
    log = "pause_log" + str(R) + ".txt"

    pause_vec = []
    unpause_vec = []
    filename = directory + log
    j = 0

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            if job in line:
                # found job
                break
            else:
                # read next line
                line = f.readline()

        pause_line = f.readline()
        unpause_line = f.readline()
        
        # convert ts_pause to list of seconds
        ts_pause = pause_line.split(', ')       # vector of timestaps
        for i in range(len(ts_pause)):  
            if i == len(ts_pause) - 1:
                ts_pause[i] = ts_pause[i].split(',\n')[0]
            t = ts_pause[i].split(':')
            t = 3600 * int(t[0]) + 60 * int(t[1]) + float(t[2])
            ts_pause[i] = round(t, 2)

        # convert ts_unpause to list of seconds
        ts_unpause = unpause_line.split(', ')       # vector of timestaps
        for i in range(len(ts_unpause)):
            if i == len(ts_unpause) - 1:
                ts_unpause[i] = ts_unpause[i].split(',\n')[0]
            t = ts_unpause[i].split(':')
            t = 3600 * int(t[0]) + 60 * int(t[1]) + float(t[2])
            ts_unpause[i] = round(t, 2)

        # convert to numpy array
        ts_pause = np.array(ts_pause)
        ts_unpause = np.array(ts_unpause)

        return ts_pause, ts_unpause


def format_plot(ax1, ax2):
    '''
        format line plot as specified in task description.
        2 y axes
    '''
    # axes (ax1 = cpus, ax2 = QPS)
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("#cores used by memcached", rotation=0)
    ax2.set_ylabel("QPS", rotation=0)
    ax1.yaxis.set_label_coords(0.001, 1.02)
    ax2.yaxis.set_label_coords(1, 1.06)

    # set ax limits
    ax1.set_ylim(0, 2.5)
    ax2.set_ylim(0, 110000)
    # TODO: set x_axis limit to computed value
    ax1.set_xlim(-5, 880)

    # grid and background
    ax1.set_facecolor((0.95, 0.95, 0.95))
    ax1.set_axisbelow(True)
    ax1.grid(axis='x', color='white', linewidth=1.0)

    # set ax2 yticks and color
    ax2.set_yticks(np.arange(0, 110000, 5000), labels=None, minor=True)
    ax2.set_yticks(np.arange(0, 110000, 10000), labels=["0","10K", "20K", "30K", "40K", "50K", "60K", "70K", "80K", "90K", "100K"])
    ax2.tick_params(axis='y', colors='grey')

    # set ax1 yticks and color
    ax1.set_yticks(np.arange(0, 2.5, 0.5), labels=None, minor=True)
    ax1.set_yticks(np.arange(0, 3, 1), labels=["0","1", "2"])
    ax1.tick_params(axis='y', colors='darkblue')

    # set xticks
    ax1.set_xticks(np.arange(0, 880, 50), labels=None, minor=True)
    ax1.set_xticks(np.arange(0, 870, 100))


def format_schedule_plot(fig_ax):
    '''
        format bar chart of schedule (parsec jobs)
    '''

    fig_ax.set_title("Plot B, run " + str(R) + ": Scheduling policy according to dynamic scheduler and variable load", loc='left', pad=40)

     # TODO: set x_axis limit to computed value
    fig_ax.set_xlim(-5, 880)
    fig_ax.set_ylim(0.25, 1.25)
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.set_axisbelow(True)
    fig_ax.grid(axis='x', color='white', linewidth=1.0)

    # set x labels
    fig_ax.set_xticks(np.arange(0, 880, 50), labels=None, minor=True)
    fig_ax.set_xticks(np.arange(0, 870, 100))

    # set y labels
    fig_ax.set_yticks([0.5, 1], labels=["core 2 & 3", "core 1"])



def main():

    fig, ax = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2.5]}, figsize=(10, 7))
    #---------------------------------------------------------
    # call the fill_table script to get the execution times (columns of times are runs, rows are jobs in job_order)
    job_order, t_start, t_end, t_exec = fill_table.main()
    t_start = t_start[:, R-1]
    t_end = t_end[:, R-1]
    t_exec = t_exec[:, R-1]

    # get QPS and latencies from mcperf (100x3 matrices)
    latencies, qps = load_mcperf_data()

    # get memcached jumps
    x_jumps, y_jumps = load_cpu_jumps(R-1)

    # xvalues for latencies and qps
    #TODO: set this value accordig to computed value
    x_vals = np.arange(0, 870, 10)
   
    # ---------------------------------plot schedule bar chart (upper plot)------------------------------------------------------
    # in order of job_order
    colors = ['lightblue', 'limegreen', 'palegoldenrod', 'firebrick', 'thistle', 'mediumturquoise', 'goldenrod']

    # TODO: use the same as in extract_data.sh
    cat1 = ['dedup', 'radix', 'blackscholes']           # pausing happens
    cat2 = ['ferret', 'freqmine', 'canneal', 'vips']    # no pausing

    # normlize start times
    global_min = min(t_start)
    t_start_norm = t_start - global_min
    t_end_norm = t_start_norm + t_exec
    x_jumps_norm = x_jumps - global_min

    # format plot
    format_schedule_plot(ax[0])

    # plot data
    for i in range(len(job_order)):
        job = job_order[i]
        # category 1 jobs
        if job in cat1:
            pause, unpause = load_cat1_data(job)
            
            start_times = np.append(t_start[i], unpause)
            start_times_norm = start_times - global_min
            end_times = np.append(pause, t_end[i])
            end_times_norm = end_times - global_min
            # width of bars
            timespans = end_times_norm - start_times_norm
        
            for l in range(len(timespans)):
                ax[0].barh(1, width=timespans[l], height=0.25, left=start_times_norm[l], align='center', color=colors[i], alpha=1)
        # category 2 jobs
        else:
            ax[0].barh(0.5, width=t_end_norm[i]-t_start_norm[i], height=0.25, left=t_start_norm[i], align='center', color=colors[i], alpha=1)

    # # add vertical lines for start of jobs
    # for j in range(len(job_order)):
    #     ax[0].axvline(x=t_start_norm[j], color=colors[j], linestyle='dotted', linewidth=1.5)

    # manually create legend
    legend_elems = []
    for n in range(len(job_order)):
        elem = Patch(facecolor=colors[n], label=job_order[n])
        legend_elems.append(elem)
    ax[0].legend(handles=legend_elems, ncol=len(job_order), bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')

    # find parameter to cut graph
    schedule_end = max(t_end_norm)
    print("cut lower graph at: ", schedule_end + 60)
    print("total time: ", schedule_end)
    #TODO: set x_axis limit to computed value
    #----------------------------------------------------------------------------------------------------------------
    # ---------------------------------plot #cores and qps (lower plot)------------------------------------------
    ax2 = ax[1].twinx()
    format_plot(ax[1], ax2)

    # # SLO line
    # x_slo = np.linspace(-50, 1050, 100)
    # y_slo = np.ones(100)
    # ax[1].plot(x_slo, y_slo, color='royalblue', linestyle='--', linewidth=1.0, label='SLO')

    # plot cores used (ax1) and qps (ax2)
    ax[1].step(np.append(x_jumps_norm, 870), np.append(y_jumps, 2), where='post', color='darkblue', marker='o', mec='white', mew=0.7, ms=4.0, linewidth=0.6, label='core usage change')
    ax2.plot(x_vals, qps[0:87, R-1], color='grey', marker='h', mec='white', mew=0.7, ms=4.5, linewidth=1.5, label='QPS', alpha=0.5)

    # add vertical lines for start of jobs
    for j in range(len(job_order)):
        ax[1].axvline(x=t_start_norm[j], color=colors[j], linestyle='dotted', linewidth=1.5)

    # legend
    lines, labels = ax[1].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, ncol=3, loc='upper right', fontsize='small')
    #----------------------------------------------------------------------------------------------------------------
    
    plt.tight_layout()
    plt.savefig('plot_4_3_B_' + str(R) + '.pdf')

    return


if __name__ == "__main__":
    main()