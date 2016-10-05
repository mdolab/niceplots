from __future__ import division
import matplotlib.pyplot as plt
import numpy as np


def handle_close(evt):
    """ Handler function that saves the figure as a pdf if the window is closed. """
    plt.tight_layout()
    plt.savefig('figure.pdf')

def adjust_spines(ax = None, spines=['left', 'bottom'], off_spines=['top', 'right']):
    """ Function to shift the axes/spines so they have that offset
        Doumont look. """
    if ax == None:
        ax = plt.gca()

    # Loop over the spines in the axes and shift them
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 18))  # outward by 18 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])

    for spine in off_spines:
        ax.spines[spine].set_visible(False)


def draggable_legend(axis = None, color_on = True):
    """ Function to create draggable labels on a plot. """
    if axis == None:
        axis = plt.gca()

    # Get the limits and relevant parameters
    xlim = axis.get_xlim()
    ylim = axis.get_ylim()
    xl, yl = xlim[1] - xlim[0], ylim[1] - ylim[0]
    legend = []
    nlines = len(axis.lines)

    # Set the coordinates of the starting location of the draggable labels
    n = np.ceil(np.sqrt(nlines))
    lins = np.linspace(.1, .9, n)
    xs, ys = np.meshgrid(lins, lins)
    xs = xs.reshape(-1)
    ys = ys.reshape(-1)
    coords = np.zeros(2)

    # Loop over each line in the plot and create a label
    for idx, line in enumerate(axis.lines):

        # Set the starting coordinates of the label
        coords[0] = xs[idx]
        coords[1] = ys[idx]
        label = line.get_label()

        # Get the color of each line to set the label color as the same
        if color_on:
            color = line.get_color()
        else:
            color = 'k'

        # Set each annotation and make them draggable
        legend.append(axis.annotate(label, xy=coords,
                   ha="center", va="center", color=color,
                   xycoords='axes fraction'
                   ))
        legend[idx].draggable()

from matplotlib.lines import Line2D
import random

def horiz_bar(labels, times, header, ts=1, nd=1, size=[5, .5], color='#FFCC00'):
    """ Creates a horizontal bar chart to compare positive numbers.

    'labels' contains the ordered labels for each data set
    'times' contains the numerical data for each entry
    'header' contains the left and right header for the labels and
    numeric data, respectively
    'ts' is a scaling parameter that's useful when the labels
    have many skinny or wide characters
    'nd' is the number of digits to show after the decimal point for the data
    'size' is the size of the final figure (iffy results)
    'color' is a hexcode for the color of the scatter points used

    """

    # Obtain parameters to size the chart correctly
    num = len(times)
    width = size[0]
    height = size[1] * num
    t_max = max(times)
    l_max = len(max(labels, key=len))

    # Create the corresponding number of subplots for each individual timing
    fig, axarr = plt.subplots(num, 1)

    # Playing with these values here can help with label alignment
    left_lim = -ts*l_max*.038*t_max
    right_lim = t_max*1.11

    # These values tweak the header label placement
    left_header_pos = -len(header[0])*.018*t_max + left_lim/2
    right_header_pos = -len(header[1])*.018*t_max + right_lim + t_max*(.09+nd*.02)

    # Loop over each time and get the max number of digits
    t_max_digits = 0
    for t in times:
        tm = len(str(int(t)))
        if tm > t_max_digits:
            t_max_digits = tm

    # Actual loop that draws each bar
    for j,(l,t,ax) in enumerate(zip(labels, times, axarr)):

        # Draw the gray line and singular yellow dot
        ax.axhline(y=1, c='#C0C0C0', lw=3, zorder=0)
        ax.scatter([t],[1], c=color, lw=0, s=100, zorder=1, clip_on=False)

        # Set chart properties
        ax.set_ylim(.99, 1.01)
        ax.set_xlim(0, t_max*1.05)
        ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,      # ticks along the bottom edge are off
            labelleft=False,
            labelright=False,
            labelbottom=False,
            right=False,         # ticks along the top edge are off
            bottom=j==num,
            top=False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.text(left_lim, 1, l, va='center')
        d = t_max_digits - len(str(int(t)))
        exec("string = '  ' * d + '%0.{}f'%t".format(nd))
        ax.text(right_lim, 1, string, va='center')

        # Create border graphics if this is the top bar line
        if j == 0:
            ax.text(left_header_pos,1.02, header[0], fontsize=13)
            ax.text(right_header_pos,1.02, header[1], fontsize=13)

            line = Line2D([left_lim, right_lim+t_max*(.15+nd*.02)], [1.012, 1.012], lw=1.2, color='k')
            line.set_clip_on(False)
            ax.add_line(line)

            line = Line2D([left_lim, right_lim+t_max*(.15+nd*.02)], [1.01, 1.01], lw=1.2, color='k')
            line.set_clip_on(False)
            ax.add_line(line)

    # Save the figure and export as pdf
    fig.set_size_inches(width, height)
    fig.savefig('bar_chart.pdf', bbox_inches="tight")

def all():
    """ Runs all of the functions provided in this module. """
    adjust_spines()
    draggable_legend()
    viridis()
    plt.gcf().canvas.mpl_connect('close_event', handle_close)
