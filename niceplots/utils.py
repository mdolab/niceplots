from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from cycler import cycler
from collections import OrderedDict


def setRCParams():
    # Set some defaults for generating nice, Doumont-esque, plots
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["CMU Bright"]
    plt.rcParams["font.size"] = 24
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["figure.figsize"] = [12, 6.75]
    plt.rcParams["savefig.dpi"] = 600
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.labelpad"] = 8.0
    plt.rcParams["text.latex.preamble"] = r"\usepackage{cmbright}"

    plt.rcParams["legend.columnspacing"] = 0.2
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["figure.constrained_layout.use"] = True

    plt.rcParams["patch.edgecolor"] = "w"

    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False

    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["axes.xmargin"] = 0
    plt.rcParams["axes.ymargin"] = 0

    plt.rcParams["lines.linewidth"] = 2.0

    niceColors = get_niceColors()
    plt.rcParams["axes.prop_cycle"] = cycler("color", niceColors.values())
    plt.rcParams["axes.edgecolor"] = niceColors["Grey"]
    plt.rcParams["text.color"] = niceColors["Grey"]
    plt.rcParams["axes.labelcolor"] = niceColors["Grey"]
    plt.rcParams["axes.labelweight"] = 200
    plt.rcParams["xtick.color"] = niceColors["Grey"]
    plt.rcParams["ytick.color"] = niceColors["Grey"]


def get_niceColors():
    # Define an ordered dictionary of some nice Doumont style colors to use as the default color cycle
    niceColors = OrderedDict()
    niceColors["Yellow"] = "#e29400ff"  # '#f8a30dff'
    niceColors["Blue"] = "#1E90FF"
    niceColors["Red"] = "#E21A1A"
    niceColors["Green"] = "#00a650ff"
    niceColors["Maroon"] = "#800000ff"
    niceColors["Orange"] = "#E64616"
    niceColors["Purple"] = "#800080ff"
    niceColors["Cyan"] = "#00A6D6"
    niceColors["Grey"] = "#5a5758ff"
    niceColors["Black"] = "#000000ff"

    return niceColors


def get_delftColors():
    # Define an ordered dictionary of the official TU Delft colors to use as the default color cycle
    delftColors = OrderedDict()
    delftColors["Cyan"] = "#00A6D6"  # '#f8a30dff'
    delftColors["Yellow"] = "#E1C400"
    delftColors["Purple"] = "#6D177F"
    delftColors["Red"] = "#E21A1A"
    delftColors["Green"] = "#A5CA1A"
    delftColors["Blue"] = "#1D1C73"
    delftColors["Orange"] = "#E64616"
    delftColors["Grey"] = "#5a5758ff"
    delftColors["Black"] = "#000000ff"

    return delftColors


def handle_close(evt):
    """Handler function that saves the figure as a pdf if the window is closed."""
    plt.tight_layout()
    plt.savefig("figure.pdf")


def adjust_spines(ax=None, spines=["left", "bottom"], outward=True):
    """Function to shift the axes/spines so they have that offset
    Doumont look."""
    if ax is None:
        ax = plt.gca()

    # Loop over the spines in the axes and shift them
    for loc, spine in ax.spines.items():
        if loc in spines:
            ax.spines[loc].set_visible(True)
            if outward:
                spine.set_position(("outward", 12))  # outward by 18 points
        else:
            ax.spines[loc].set_visible(False)  # don't draw spine

    # turn off ticks where there is no spine
    if "left" in spines:
        ax.yaxis.set_ticks_position("left")
    elif "right" in spines:
        ax.yaxis.set_ticks_position("right")
    else:
        # no yaxis ticks
        ax.yaxis.set_visible(False)

    if "bottom" in spines:
        ax.xaxis.set_ticks_position("bottom")
    elif "top" in spines:
        ax.xaxis.set_ticks_position("top")
    else:
        # no xaxis ticks
        # ax.xaxis.set_ticks([])
        ax.xaxis.set_visible(False)


def draggable_legend(axis=None, color_on=True):
    """Function to create draggable labels on a plot."""
    if axis is None:
        axis = plt.gca()

    # Get relevant parameters
    legend = []
    nlines = len(axis.lines)

    # Set the coordinates of the starting location of the draggable labels
    n = np.ceil(np.sqrt(nlines))
    lins = np.linspace(0.1, 0.9, n)
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
            color = "k"

        # Set each annotation and make them draggable
        legend.append(
            axis.annotate(
                label,
                xy=coords,
                ha="center",
                va="center",
                color=color,
                xycoords="axes fraction",
            )
        )
        legend[idx].draggable()


def horiz_bar(labels, times, header, ts=1, nd=1, size=[5, 0.5], color="#FFCC00"):
    """Creates a horizontal bar chart to compare positive numbers.

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
    left_lim = -ts * l_max * 0.038 * t_max
    right_lim = t_max * 1.11

    # These values tweak the header label placement
    left_header_pos = -len(header[0]) * 0.018 * t_max + left_lim / 2
    right_header_pos = -len(header[1]) * 0.018 * t_max + right_lim + t_max * (0.09 + nd * 0.02)

    # Loop over each time and get the max number of digits
    t_max_digits = 0
    for t in times:
        tm = len(str(int(t)))
        if tm > t_max_digits:
            t_max_digits = tm

    # Actual loop that draws each bar
    for j, (l, t, ax) in enumerate(zip(labels, times, axarr)):

        # Draw the gray line and singular yellow dot
        ax.axhline(y=1, c="#C0C0C0", lw=3, zorder=0)
        ax.scatter([t], [1], c=color, lw=0, s=100, zorder=1, clip_on=False)

        # Set chart properties
        ax.set_ylim(0.99, 1.01)
        ax.set_xlim(0, t_max * 1.05)
        ax.tick_params(
            axis="both",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            left=False,  # ticks along the bottom edge are off
            labelleft=False,
            labelright=False,
            labelbottom=False,
            right=False,  # ticks along the top edge are off
            bottom=j == num,
            top=False,
        )
        ax.spines["top"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.text(left_lim, 1, l, va="center")
        # d = t_max_digits - len(str(int(t)))
        string = "{number:.{digits}f}".format(number=t, digits=nd)
        ax.text(right_lim * 1.15, 1, string, va="center", ha="right")

        # Create border graphics if this is the top bar line
        if j == 0:
            ax.text(left_header_pos, 1.02, header[0], fontsize=13)
            ax.text(right_header_pos, 1.02, header[1], fontsize=13)

            line = Line2D(
                [left_lim, right_lim + t_max * (0.15 + nd * 0.03)],
                [1.014, 1.014],
                lw=1.2,
                color="k",
            )
            line.set_clip_on(False)
            ax.add_line(line)

            # line = Line2D([left_lim, right_lim+t_max*(.15+nd*.03)], [1.012, 1.012], lw=1.2, color='k')
            # line.set_clip_on(False)
            # ax.add_line(line)

    # Save the figure and export as pdf
    fig.set_size_inches(width, height)


def stacked_plots(
    xlabel,
    xdata,
    data_dict_list,
    figsize=(12, 10),
    outward=True,
    filename="stacks.png",
    xticks=None,
    cushion=0.1,
    colors=None,
    lines_only=False,
    line_scaler=1.0,
    xlim=None,
    dpi=200,
):

    # If it's a dictionary, make it into a list so we can generically loop over it
    if isinstance(data_dict_list, dict):
        data_dict_list = [data_dict_list]

    if colors is None:
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    data_dict = data_dict_list[0]
    n = len(data_dict)

    f, axarr = plt.subplots(n, figsize=figsize)

    for i, (ylabel, ydata) in enumerate(data_dict.items()):
        if type(ydata) == dict:
            if "limits" in ydata.keys():
                axarr[i].set_ylim(ydata["limits"])
            elif "ticks" in ydata.keys():
                axarr[i].set_yticks(ydata["ticks"])
                low_tick = ydata["ticks"][0]
                high_tick = ydata["ticks"][-1]
                height = high_tick - low_tick
                limits = [low_tick - cushion * height, high_tick + cushion * height]
                axarr[i].set_ylim(limits)

        axarr[i].set_ylabel(ylabel, rotation="horizontal", horizontalalignment="right")

        # Doesn't correctly work when we give a dict version
        if xlim is not None:
            if type(ydata) == dict:
                ydata = ydata["data"]
            ydata = np.array(ydata, dtype="float")
            no_nan_y = ydata[np.isfinite(ydata)]
            ylim = [np.mean(no_nan_y), np.mean(no_nan_y)]
            axarr[i].scatter(list(xlim), ylim, alpha=0.0)

    for j, data_dict in enumerate(data_dict_list):
        for i, (ylabel, ydata) in enumerate(data_dict.items()):
            if type(ydata) == dict:
                ydata = ydata["data"]
            axarr[i].plot(xdata, ydata, clip_on=False, lw=6 * line_scaler, color=colors[j])
            if not lines_only:
                axarr[i].scatter(
                    xdata,
                    ydata,
                    clip_on=False,
                    edgecolors="white",
                    s=100 * line_scaler ** 2,
                    lw=1.5 * line_scaler,
                    zorder=100,
                    color=colors[j],
                )

    for i, ax in enumerate(axarr):
        adjust_spines(ax, outward=outward)
        if i < len(axarr) - 1:
            ax.xaxis.set_ticks([])
        else:
            ax.xaxis.set_ticks_position("bottom")
            if xticks is not None:
                ax.xaxis.set_ticks(xticks)

    f.align_labels()
    axarr[-1].set_xlabel(xlabel)

    # plt.tight_layout()

    if "png" in filename:
        plt.savefig(filename, bbox_inches="tight", dpi=dpi)
    else:
        plt.savefig(filename, bbox_inches="tight")

    return f, axarr


def all():
    """Runs all of the functions provided in this module."""
    adjust_spines()
    draggable_legend()
    plt.gcf().canvas.mpl_connect("close_event", handle_close)
