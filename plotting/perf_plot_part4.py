#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
from pandas import *
import matplotlib.pyplot as plt
import os


# In[145]:


def load_data(cpu, thread):
    ''' 
        load data of all three runs of given config 
        (y_vals given in [mikro_s])
        returns: vector of averaged x_vals (25x1), vector of averaged x_vals (25x1)
                 vector of x_std errors (25x1) and cevtor of y_std errors (25x1)   
    '''
    x_vals = np.empty([3,25])
    y_vals = np.empty([3,25])
    
    # x_vals: 95th percentile (tail latency), y_vals: actual QPS
    for i in range(3):
        filename = "cpu" + str(cpu) + 'thread' + str(thread) + '_run' + str(i+1) + '.csv'
        data = read_csv(filename)
        data.drop(data.tail(2).index,inplace=True)
        y_val = data['p95'].to_numpy()
        x_val = data['QPS'].to_numpy()
        y_vals[i] = y_val
        x_vals[i] = x_val
        
    return x_vals.mean(axis=0), y_vals.mean(axis=0), np.std(x_vals, axis=0), np.std(y_vals,axis=0)


# In[146]:


def format_plot(fig_ax):
    fig_ax.set_xlabel("Queries per second (QPS)")
    fig_ax.set_ylabel("$\mathregular{95^{th}}$ percentile latency [μs]", rotation=0)
    fig_ax.yaxis.set_label_coords(0.001, 1.02)
    fig_ax.set_facecolor((0.95, 0.95, 0.95))
    fig_ax.grid(axis='y', color='white', linewidth=1.0)
    fig_ax.grid(which='both', axis='x', color='white', linewidth=1.0)
    fig_ax.set_xticks(np.arange(0, 130000, 5000), labels=None, minor=True)
    fig_ax.set_xticks(np.arange(0, 130000, 10000), labels=["0","10K", "20K", "30K", "40K", "50K", "60K", "70K", "80K", "90K", "100K", "110K", "120K"])

    #Title
    fig_ax.set_title("Impact of number of allocated cores and threads on tail latency of 'memcached' application", loc='left', pad=40)


# In[147]:


def main():
    configurations = [[1,1], [1,2], [2,1], [2,2]]
    colors = ['red', 'mediumblue', 'forestgreen', 'goldenrod']
    labels = ["C=1 T=1", "C=1 T=2", "C=2 T=1", "C=2 T=2"]
    markers = ['o', 'h', 'D', 'v']

    #Create Plot
    fig = plt.figure(figsize=(9, 7))
    fig_ax = fig.gca()
    format_plot(fig_ax)

    for i in range(len(configurations)):
        x_val, y_val, x_err, y_err = load_data(configurations[i][0],configurations[i][1])

        fig_ax.errorbar(x_val, y_val, xerr=x_err, yerr=y_err, ecolor=colors[i], elinewidth=0.6, barsabove=False, capsize=2, capthick=1, fmt='none', mec='white', mew=0.4, alpha=0.8)
        fig_ax.plot(x_val, y_val, marker=markers[i], mec='white', mew=0.7, ms=4.5, c=colors[i], linewidth=1.2, label=labels[i], alpha=0.8)
        print(labels[i], ' num_points used: ', len(x_val))

    fig_ax.legend(title='Configuration: ', loc='upper right')
    plt.tight_layout()
    plt.savefig("Part4_1.pdf")
    
    return


if __name__ == "__main__":
    main()


