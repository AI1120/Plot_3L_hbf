#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from math import ceil 


def _ax_plot(ax, x, y, realRpeaks, estimatedRpeaks, secs=10, lwidth=1.5, amplitude_ecg=1.8, time_ticks=0.2,sample_rate=500, 
             m=["s", "o"], ms=[75, 25]):

    
    # EKG sinyalini çiz
    ax.plot(x, y, 'k-', linewidth=lwidth)
    
    
    # Gerçek ve tahmini R peak'leri çiz
    if realRpeaks is not None:
        realRpeaks_x = np.array(realRpeaks) / sample_rate
        
        realRpeaks_y = y[realRpeaks]
        
        ax.scatter(realRpeaks_x, realRpeaks_y-1, s = ms[0], marker=m[0], alpha=0.6, color='green', label='Corrected R Peaks')
    
    if estimatedRpeaks is not None:
        estimatedRpeaks_x = np.array(estimatedRpeaks) / sample_rate
        estimatedRpeaks_y = y[estimatedRpeaks]
        ax.scatter(estimatedRpeaks_x, estimatedRpeaks_y, s = ms[1], marker=m[1], alpha=0.9, color='blue', label='Estimated R Peaks')
    
    # Eksenler ve ızgara ayarları
    ax.set_xticks(np.arange(0, secs + 1, time_ticks))
    ax.xaxis.set_major_locator(MaxNLocator(60))
    ax.yaxis.set_major_locator(MaxNLocator(9))
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle='-', linewidth='0.5', color=(1, 0.7, 0.7))
    ax.set_xlim(0, secs)

#lead_index = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']

lead_index = ['Lead 1', 'Lead 2', 'Lead 3']

def plot_12(ecg, sample_rate=500, title='ECG 3 Lead', fontsize = 8, sec=10,
            lead_index= None, # ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'], 
            lead_order=None, columns=1, speed=50, voltage=20, line_width=0.6,  correctedRPeaks=None, estimatedRpeaks=None, 
            m=["s", "o"], ms=[75, 25]):
    """Çoklu EKG grafiği çizdirme fonksiyonu."""
    plt.rcParams.update({'font.size': fontsize})
    fig, axs = plt.subplots(ceil(len(lead_index)/columns), columns, figsize=((speed/25)*sec*columns, (4.1*voltage/25)*len(lead_index)/columns), sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0, wspace=0.04, left=0.14, right=0.98, bottom=0.06, top=0.95)
    fig.suptitle(title)

    if not lead_order:
        lead_order = lead_index

    for i, ax in enumerate(axs.flat):
        t_lead = lead_order[i]  #Tüm kanallar için açıktı
        x = np.arange(0, len(ecg[t_lead].values)/sample_rate, 1/sample_rate)
        _ax_plot(ax, x, ecg[t_lead].values,correctedRPeaks[t_lead], estimatedRpeaks[t_lead], secs=sec, lwidth=line_width, amplitude_ecg=1.8, time_ticks=0.2, m=m, ms=ms)
        ax.set_ylabel(t_lead)
        if i == 0:  
            ax.legend()
       

def plot(
        ecg, 
        sample_rate    = 500, 
        title          = 'ECG 12', 
        lead_index     = lead_index, 
        lead_order     = None,
        style          = None,
        columns        = 1,
        row_height     = 10,
        show_lead_name = True,
        show_grid      = True,
        show_separate_line  = True,
        filename       = None,
        ):
    if not lead_order:
        lead_order = list(range(0,len(ecg)))
    secs  = len(ecg[0])/sample_rate
    
    leads = len(lead_order)
    rows  = int(ceil(leads/columns))
    display_factor = 1
    line_width = 1
    fig, ax = plt.subplots(figsize=(secs*columns * display_factor, rows * row_height / 5 * display_factor))

    x_min = 0
    x_max = columns * secs
    ax.set_xticks(np.arange(0, x_max + 2, 2))  # Set major ticks for every 2 seconds
    ax.set_xticklabels([f'{int(x)}s' for x in np.arange(0, x_max + 2, 2)], fontsize=12)

    ax.set_xlabel('Time (s)')
    ax.set_yticklabels([])  # Remove y-axis labels

    # Set y-axis limits based on rows and row height
    y_min = row_height / 4 - (rows / 2) * row_height
    y_max = row_height / 4
    
    # Drawing bottom ticks every 2 seconds with lines
    for x in np.arange(0, x_max + 2, 2):
        ax.vlines(x=x, ymin=y_min-0.3, ymax=y_min+0.3, color='black', linewidth=2.5)  # Bottom marks
    # Customize tick marks at the bottom for every 2 seconds
    # ax.tick_params(axis='x', which='major', length=10, width=2, direction='out', bottom=True)  # Major ticks
    # ax.tick_params(axis='x', which='minor', length=0)  # Remove minor ticks

    # Add numbered segment markers (#1 at 0 sec, #2 at 2 sec, etc.)
    for i, x in enumerate(np.arange(0, 22, 2)):  # up to last second
        ax.text(x + 0.1, y_max - 0.4, f'#{i+1}', fontsize=12, fontweight='bold', color='red')

    display_factor = display_factor ** 0.5
    fig.subplots_adjust(
        hspace = 0, 
        wspace = 0,
        left   = 0,
        right  = 1,
        bottom = 0,
        top    = 1
    )

    fig.suptitle(title)

    if (style == 'bw'):
        color_major = (0.4,0.4,0.4)
        color_minor = (0.75, 0.75, 0.75)
        color_line  = (0,0,0)
    else:
        color_major = (1,0,0)
        color_minor = (1, 0.7, 0.7)
        color_line  = (0,0,0.7)

    if(show_grid):
        ax.set_xticks(np.arange(x_min,x_max,0.2))    
        ax.set_yticks(np.arange(y_min,y_max,0.5))

        ax.minorticks_on()
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)
        
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)

    for c in range(0, columns):
        for i in range(0, rows):
            if (c * rows + i < leads):
                y_offset = -(row_height/2) * ceil(i % rows)

                x_offset = 0
                if(c > 0):
                    x_offset = secs * c
                    if(show_separate_line):
                        ax.plot([x_offset, x_offset], 
                                [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3], 
                                linewidth=line_width * display_factor, color=color_line)

                t_lead = lead_order[c * rows + i]

                step = 1.0 / sample_rate
                if(show_lead_name):
                    ax.text(x_offset + 0.07, y_offset - 0.5, lead_index[t_lead], fontsize=9 * display_factor)

                ax.plot(
                    np.arange(0, len(ecg[t_lead]) * step, step) + x_offset, 
                    ecg[t_lead] + y_offset,
                    linewidth=line_width * display_factor, 
                    color=color_line
                )
    # Save the plot as a PDF
    fig.savefig(filename, format='pdf', bbox_inches='tight')
    plt.close(fig)
                

def plot_1(ecg, sample_rate=500, title = 'ECG', fig_width = 15, fig_height = 2, line_w = 0.5, ecg_amp = 1.8, timetick = 0.2):
    """Plot multi lead ECG chart.
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        fig_width  : The width of the plot
        fig_height : The height of the plot
    """
    plt.figure(figsize=(fig_width,fig_height))
    plt.suptitle(title)
    plt.subplots_adjust(
        hspace = 0, 
        wspace = 0.04,
        left   = 0.04,  # the left side of the subplots of the figure
        right  = 0.98,  # the right side of the subplots of the figure
        bottom = 0.2,   # the bottom of the subplots of the figure
        top    = 0.88
        )
    seconds = len(ecg)/sample_rate

    ax = plt.subplot(1, 1, 1)
    #plt.rcParams['lines.linewidth'] = 5
    step = 1.0/sample_rate
    _ax_plot(ax,np.arange(0,len(ecg)*step,step),ecg, seconds, line_w, ecg_amp,timetick)
    
DEFAULT_PATH = './'
show_counter = 1

def show_svg(tmp_path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        tmp_path: path for temporary saving the result svg file
    """ 
    global show_counter
    file_name = tmp_path + "show_tmp_file_{}.svg".format(show_counter)
    plt.savefig(file_name)
    os.system("open {}".format(file_name))
    show_counter += 1
    plt.close()


def show():
    plt.show()


def save_as_png(file_name, path = DEFAULT_PATH, dpi = 100, layout='tight'):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
        dpi      : set dots per inch (dpi) for the saved image
        layout   : Set equal to "tight" to include ax labels on saved image
    """
    plt.ioff()
    plt.savefig(path + file_name + '.png', dpi = dpi, bbox_inches=layout)
    plt.close()


def save_as_svg(file_name, path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.svg')
    plt.close()


def save_as_jpg(file_name, path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.jpg')
    plt.close()

def save_as_pdf(file_name, path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.pdf')
    plt.close()