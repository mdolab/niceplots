from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

def handle_close(evt):
    plt.tight_layout()
    plt.savefig('figure.pdf')

def adjust_spines(ax = None, spines=['left', 'bottom'], off_spines=['top', 'right']):
    if ax == None:
        ax = plt.gca()

    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 18))  # outward by 10 points
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
    if axis == None:
        axis = plt.gca()

    xlim = axis.get_xlim()
    ylim = axis.get_ylim()
    xl, yl = xlim[1] - xlim[0], ylim[1] - ylim[0]
    legend = []
    nlines = len(axis.lines)
    coords = np.zeros((nlines, 2))

    n = np.ceil(np.sqrt(nlines))
    lins = np.linspace(.1, .9, n)
    xs, ys = np.meshgrid(lins, lins)
    xs = xs.reshape(-1)
    ys = ys.reshape(-1)

    for idx, line in enumerate(axis.lines):
        data_length = len(line.get_data()[0])
        data_loc = int(data_length*(idx+.5)/nlines)
        coords[idx, :] = line.get_data()[0][data_loc], line.get_data()[1][data_loc]
        nx_coord = line.get_data()[0][data_loc+1], line.get_data()[1][data_loc+1]

        coords[idx, 0] = xs[idx]
        coords[idx, 1] = ys[idx]
        label = line.get_label()

        if color_on:
            color = line.get_color()
        else:
            color = 'k'

        legend.append(axis.annotate(label, xy=coords[idx],
                   ha="center", va="center", color=color,
                   xycoords='axes fraction'
                   ))
        legend[idx].draggable()

def all():
    adjust_spines()
    draggable_legend()
    viridis()
    plt.gcf().canvas.mpl_connect('close_event', handle_close)
