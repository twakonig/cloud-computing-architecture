#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
from pandas import *
import matplotlib.pyplot as plt
import os
from matplotlib import rc
rc('mathtext', default='regular')


# In[4]:


def load_data(cpu, thread):
    ''' 
        load data of all three runs of given config 
        (y_vals given in [mikro_s])
        returns: vector of averaged x_vals (25x1), vector of averaged x_vals (25x1)
                 vector of x_std errors (25x1) and cevtor of y_std errors (25x1)   
    '''
    x_vals = np.empty([3,25])
    y_vals = np.empty([3,25])
    cpu_vals = np.empty([3,25])
    
    # x_vals: 95th percentile (tail latency), y_vals: actual QPS
    for i in range(3):
        filename = "cpu" + str(cpu) + 'thread' + str(thread) + '_run' + str(i+1) + '.csv'
        data = read_csv(filename)
        data.drop(data.tail(2).index,inplace=True)
        cpu_val = data['CPU'].to_numpy()
        y_val = data['p95'].to_numpy()
        x_val = data['QPS'].to_numpy()
        y_vals[i] = y_val
        x_vals[i] = x_val
        cpu_vals[i] = cpu_val
        
    return x_vals.mean(axis=0), y_vals.mean(axis=0), cpu_vals.mean(axis=0)


# In[66]:


def format_plot(ax1,ax2,i):
    percentile_limits = [1800,1200]
    cpu_limits = [100,150]
    
    ax1.set_xlabel("Queries per second (QPS)")
    ax1.set_ylabel("$\mathregular{95^{th}}$ percentile latency [μs]", rotation=0)
    ax2.set_ylabel("CPU Utilization %", rotation=0)

    ax1.yaxis.set_label_coords(0.001, 1.02)
    ax2.yaxis.set_label_coords(1, 1.06)
    
    ax1.set_facecolor((0.95, 0.95, 0.95))
    ax1.grid(axis='y', color='white', linewidth=1.0)
    ax1.grid(which='both', axis='x', color='white', linewidth=1.0)
    
    ax1.set_xticks(np.arange(0, 130000, 5000), labels=None, minor=True)
    ax1.set_xticks(np.arange(0, 140000, 10000), labels=["0","10K", "20K", "30K", "40K", "50K", "60K", "70K", "80K", "90K", "100K", "110K", "120K","130K"])
    ax1.tick_params(axis='y', colors='#2D2DB9')
    
    ax2.tick_params(axis='y', colors='#A03232')
    ax1.set_xlim(0,130000)
    ax2.set_ylim(0,cpu_limits[i])
    ax1.set_ylim(0,percentile_limits[i])
    
    #Title
    ax1.set_title("CPU utilization and tail latency of 'memcached' with C="+str(i+1), loc='center', pad=40)



# In[68]:


def main():
    colors = ['#2D2DB9', '#A03232','#595959']
    markers = ['o', 'h', 'D', 'v']
    x_line = np.arange(5000,130000,5000)
    y_line = np.full(25,1000)

    for i in range(2):
        x,y,cpu = load_data(i+1,2)
        fig, ax1 = plt.subplots(figsize=(9,7))

        ax2 = ax1.twinx()
        ax1.plot(x_line,y_line,'--', c=colors[2])
        format_plot(ax1,ax2,i)
        ax1.plot(x, y, marker = markers[0], mec='white', mew=0.7, ms=4.5,c=colors[0], linewidth=1.2, label='95th Percentile Latency', alpha=0.8)
        ax2.plot(x, cpu, marker = markers[1], mec='white', mew=0.7, ms=4.5,c=colors[1], linewidth=1.2, label='CPU Utilization', alpha=0.8)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')
        plt.tight_layout()
        plt.savefig("Part4_cpu"+str(i+1)+".pdf")
        
    return


if __name__ == "__main__":
    main()





