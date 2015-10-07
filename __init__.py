import matplotlib.pyplot as plt
import numpy as np

def adjust_spines(ax, spines=['left', 'bottom'], off_spines=['top', 'right']):
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


def my_legend(axis = None, color_on = True):

    if axis == None:
        axis = plt.gca()

    xlim = axis.get_xlim()
    ylim = axis.get_ylim()
    xl, yl = xlim[1] - xlim[0], ylim[1] - ylim[0]
    legend = []
    nlines = len(axis.lines)
    coords = np.zeros((nlines, 2))
    for idx, line in enumerate(axis.lines):
        data_length = len(line.get_data()[0])
        data_loc = int(data_length*(idx+.5)/nlines)
        coords[idx, :] = line.get_data()[0][data_loc], line.get_data()[1][data_loc]
        nx_coord = line.get_data()[0][data_loc+1], line.get_data()[1][data_loc+1]
        diff = nx_coord - coords[idx, :]
        diff = diff / np.sqrt(np.sum(diff**2))
        coords[idx, 0] = (coords[idx, 0] - xlim[0]) / xl - 0.075 * diff[1]
        coords[idx, 1] = (coords[idx, 1] - ylim[0]) / yl - 0.075 * diff[0]
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