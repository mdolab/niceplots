from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from cycler import cycler
from collections import OrderedDict
from .parula import parula_map
from matplotlib import patheffects
from matplotlib.collections import LineCollection
import warnings
from adjustText import adjust_text


def setRCParams(dark_mode=False, set_dark_background=False):
    """
    Set some defaults for generating nice, Doumont-esque plots.

    Inputs
    ------
    dark_mode (optional) : bool
        If true, sets axes, labels, etc. to white so the plot
        can be used on a dark background.
        NOTE: Unless you are explicitly saving the plot with
        a transparent background (e.g. as a png with
        transparent=True), also set the
        set_dark_background option.
    set_dark_background (optional) : bool or str
        If true, sets the axis and figure backgrounds to black.
        This option can also be set to a color string, such as
        "#aaaaaa", to use a color other than black.
    """
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["CMU Bright"]
    plt.rcParams["axes.unicode_minus"] = False
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
    plt.rcParams["lines.markeredgewidth"] = 1.0
    plt.rcParams["lines.markeredgecolor"] = "w"

    niceColors = get_niceColors()
    plt.rcParams["axes.prop_cycle"] = cycler("color", list(niceColors.values())[:-2])

    # Color for axes, labels, ticks, text, etc.
    color = niceColors["Grey"]
    if dark_mode:
        plt.rcParams["patch.edgecolor"] = "#000000"
        color = "#ffffff"  # white

    plt.rcParams["axes.edgecolor"] = color
    plt.rcParams["text.color"] = color
    plt.rcParams["axes.labelcolor"] = color
    plt.rcParams["axes.labelweight"] = 200
    plt.rcParams["xtick.color"] = color
    plt.rcParams["ytick.color"] = color

    # Set the axis and figure background color if necessary
    if isinstance(set_dark_background, bool):
        if set_dark_background:
            # Set background to black
            plt.rcParams["axes.facecolor"] = "#000000"
            plt.rcParams["figure.facecolor"] = "#000000"
    elif isinstance(set_dark_background, str):
        # Set background to set_dark_background
        plt.rcParams["axes.facecolor"] = set_dark_background
        plt.rcParams["figure.facecolor"] = set_dark_background
        plt.rcParams["patch.edgecolor"] = set_dark_background
    else:
        raise TypeError(f"set_dark_background value of {set_dark_background} is invalid")


def get_niceColors():
    # Define an ordered dictionary of some nice Doumont style colors to use as the default color cycle
    niceColors = OrderedDict()
    niceColors["Yellow"] = "#e29400ff"  # '#f8a30dff'
    niceColors["Blue"] = "#1E90FF"
    niceColors["Red"] = "#E21A1A"
    niceColors["Green"] = "#00a650ff"
    niceColors["Maroon"] = "#800000ff"
    niceColors["Orange"] = "#ff8f00"
    niceColors["Purple"] = "#800080ff"
    niceColors["Cyan"] = "#00A6D6"
    niceColors["Black"] = "#000000ff"
    # The 2 colours below are not used in the colour cycle as they are too close to the other colours.
    # Grey is kept in the dictionary as it is used as the default axis/tick colour.
    # RedOrange is the old Orange, and is kept because I think it looks nice.
    niceColors["Grey"] = "#5a5758ff"
    niceColors["RedOrange"] = "#E21A1A"

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
    lins = np.linspace(0.1, 0.9, int(n))
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


def auto_place_legend(ax, rel_xloc=None, color_on=True, **kwargs):
    """
    This function tries to automatically place legend text
    close to the respective line and tries to minimize the
    possible overlap with other lines and text. This function uses
    a the adjustText module.
    Inputs:
        ax : matplotlib axes
            Single matplotlib axes
        rel_xloc : list or scalar
            Relative location (between 0 and 1) on the x axis
            where to *try* to place the legend text. List has to be the
            same length as the number of lines in plot.
            If not specified random location will be chosen.
        color_on : bool
            Use the color on the line to color the legend text.
        kwargs : optional keyword arguments
            This is intended to tweak the adjustText tool (passed onwards)
    """
    nLines = len(ax.lines)

    # If using a scalar generate a full list needed for placing line label
    if type(rel_xloc) is float:
        rel_xloc = nLines * [rel_xloc]

    # Loop over the lines in the axes to get line label text and color
    texts = []
    for i, line in enumerate(ax.lines):

        # Extract the xy data (numpy Nx2 array) for a given line
        coords = line.get_xydata()

        # Set the starting x-coordinates of the label either using the
        # relative locations or randomly
        if rel_xloc is not None:
            idx = int(rel_xloc[i] * (coords[:, 0].shape[0] - 1))
        else:
            # Select randomly one point from the dataset to place the text
            idx = np.random.randint(0, coords.shape[0])

        label = line.get_label()
        # Get the color of each line to set the label color as the same
        if color_on:
            color = line.get_color()
        else:
            color = "k"

        # Create the text object and place it at this random location on line
        t = ax.text(coords[idx, 0], coords[idx, 1], label, ha="center", va="center", color=color)
        texts.append(t)

    adjust_text(texts, ax=ax, **kwargs)


def horiz_bar(labels, times, header, ts=1, nd=1, size=[5, 0.5], color=None):
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

    # Use niceColours yellow if no colour specified
    if color is None:
        color = get_niceColors()["Yellow"]

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
    right_text_x = right_lim * 1.15

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
        ax.text(right_text_x, 1, string, va="center", ha="right")

        # Create border graphics if this is the top bar line
        if j == 0:
            ax.text(left_lim, 1.02, header[0], ha="left")
            ax.text(right_text_x, 1.02, header[1], ha="right")

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
        for i, (_, ydata) in enumerate(data_dict.items()):
            if type(ydata) == dict:
                ydata = ydata["data"]
            axarr[i].plot(xdata, ydata, clip_on=False, lw=6 * line_scaler, color=colors[j])
            if not lines_only:
                axarr[i].scatter(
                    xdata,
                    ydata,
                    clip_on=False,
                    edgecolors=axarr[i].get_facecolor(),
                    s=100 * line_scaler**2,
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


def plotOptProb(
    obj,
    xRange,
    yRange,
    ineqCon=None,
    eqCon=None,
    nPoints=51,
    optPoint=None,
    conStyle="shaded",
    ax=None,
    colors=None,
    cmap=None,
    levels=None,
    labelAxes=True,
):
    """Generate a contour plot of a 2D constrained optimisation problem

    Parameters
    ----------
    obj : function
        Objective function, should accept inputs in the form f = obj(x, y) where x and y are 2D arrays
    xRange : list or array
        Upper and lower limits of the plot in x
    yRange : list or array
        Upper and lower limits of the plot in y
    ineqCon : function or list of functions, optional
        Inequality constraint functions, should accept inputs in the form g = g(x, y) where x and y are 2D arrays.
        Constraints are assumed to be of the form g <= 0
    eqCon : functions or list of functions, optional
        Equality constraint functions, should accept inputs in the form h = h(x, y) where x and y are 2D arrays.
        Constraints are assumed to be of the form h == 0
    nPoints : int, optional
        Number of points in each direction to evaluate the objective and constraint functions at
    optPoint : list or array, optional
        Optimal Point, if you want to plot a point there, by default None
    conStyle : str, optional
        Controls how inequality constraints are represented, "shaded" will shade the infeasible regions while "hashed"
        will place hashed lines on the infeasible side of the feasible boundary, by default "shaded", note the "hashed"
        option only works for matplotlib >= 3.4
    ax : matplotlib axes object, optional
        axes to plot, by default None, in which case a new figure will be created and returned by the function
    colors : list, optional
        List of colors to use for the constraint lines, by default uses the current matplotlib color cycle
    cmap : colormap, optional
        Colormap to use for the objective contours, by default will use nicePlots' parula map
    levels : list, array, int, optional
        Number or values of contour lines to plot for the objective function
    labelAxes : bool, optional
        Whether to label the x and y axes, by default True, in which case the axes will be labelled, "$X_1$" and "$X_2$"

    Returns
    -------
    fig : matplotlib figure object
        Figure containing the plot. Returned only if no input ax object is specified
    ax : matplotlib axes object, but only if no ax object is specified
        Axis with the colored line. Returned only if no input ax object is specified
    """

    # --- Create a new figure if the user did not supply an ax object ---
    returnFig = False
    if ax is None:
        fig, ax = plt.subplots()
        returnFig = True

    # --- If user provided only single inequality or equality constraint, convert it to an iterable  ---
    cons = {}
    for inp, key in zip([eqCon, ineqCon], ["eqCon", "ineqCon"]):
        if inp is not None:
            if not hasattr(inp, "__iter__"):
                cons[key] = [inp]
            else:
                cons[key] = inp
        else:
            cons[key] = []

    # --- Check that conStyle contains a supported value to avoid random conStyle arguments ---
    if conStyle.lower() not in ["shaded", "hashed"]:
        raise ValueError(f"conStyle: {conStyle} is not supported")

    # --- Check if user has a recent enough version of matplotlib to use hashed boundaries ---
    if conStyle.lower() == "hashed":
        try:
            patheffects.withTickedStroke
        except AttributeError:
            warnings.warn(
                "matplotlib >= 3.4 is required for hashed inequality constrain boundaries, switching to shaded inequality constraint style"
            )
            conStyle = "shaded"

    # --- Define some default values if the user didn't provide them ---
    if cmap is None:
        cmap = parula_map

    if colors is None:
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    nColor = len(colors)

    # --- Create grid of points for evaluating functions ---
    X, Y = np.meshgrid(np.linspace(xRange[0], xRange[1], nPoints), np.linspace(yRange[0], yRange[1], nPoints))

    # --- Evaluate objective and constraint functions ---
    Fobj = obj(X, Y)
    g = []
    for ineq in cons["ineqCon"]:
        g.append(ineq(X, Y))
    h = []
    for eq in cons["eqCon"]:
        h.append(eq(X, Y))

    # --- Plot objective contours ---
    adjust_spines(ax, outward=True)
    ax.contour(
        X,
        Y,
        Fobj,
        levels=levels,
        cmap=cmap,
    )

    # --- Plot constraint boundaries ---
    colorIndex = 0
    for conValue in g:
        contour = ax.contour(X, Y, conValue, levels=[0.0], colors=colors[colorIndex % nColor])
        if conStyle.lower() == "hashed":
            plt.setp(contour.collections, path_effects=[patheffects.withTickedStroke(angle=60, length=2)])
        elif conStyle.lower() == "shaded":
            ax.contourf(X, Y, conValue, levels=[0.0, np.inf], colors=colors[colorIndex % nColor], alpha=0.4)

        colorIndex += 1

    for conValue in h:
        ax.contour(X, Y, conValue, levels=[0.0], colors=colors[colorIndex % nColor])

    # --- Plot optimal point if provided ---
    if optPoint is not None:
        ax.plot(
            optPoint[0],
            optPoint[1],
            "o",
            color="black",
            markeredgecolor=ax.get_facecolor(),
            markersize=10,
            clip_on=False,
        )

    # --- Label axes if required ---
    if labelAxes:
        ax.set_xlabel("$x_1$")
        ax.set_ylabel("$x_2$", rotation="horizontal", ha="right")

    if returnFig:
        return fig, ax
    else:
        return


def plotColoredLine(
    x, y, c, cmap=None, fig=None, ax=None, addColorBar=False, cRange=None, cBarLabel=None, norm=None, **kwargs
):
    """Plot an XY line whose color is determined by some other variable C

    Parameters
    ----------
    x : iterable of length n
        x data
    y : iterable of length n
        y data
    c : iterable of length n
        Data for linecolor
    cmap : str or matplotlib colormap, optional
        Colormap to use for the objective contours, by default will use nicePlots' parula map
    fig : matplotlib figure object, optional
        figure to plot on, by default None, in which case a new figure will be created and returned by the function
    ax : matplotlib axes object, optional
        axes to plot on, by default None, in which case a new figure will be created and returned by the function
    addColorBar : bool, optional
        Whether to add a colorbar to the axes, by default False
    cRange : iterable of length 2, optional
        Upper and lower limit for the colormap, by default None, in which case the min and max values of c are used.
    cBarLabel : str, optional
        Label for the colormap, by default None
    norm : matplotlib.colors.Normalize, optional
        Specify colormap mapping; both this and cRange cannot be specified, it must be one or the other (or neither)

    Returns
    -------
    fig : matplotlib figure object
        Figure containing the plot. Returned only if no input ax object is specified
    ax : matplotlib axes object
        Axis with the colored line. Returned only if no input ax object is specified
    """
    returnFig = False
    if ax is None or fig is None:
        fig, ax = plt.subplots()
        returnFig = True

    if cmap is None:
        cmap = parula_map

    # --- Convert inputs to flattened arrays ---
    data = {}
    for d, name in zip([x, y, c], ["x", "y", "c"]):
        if not isinstance(d, np.ndarray):
            data[name] = np.array(d)
        else:
            data[name] = d
        data[name] = data[name].flatten()

    # --- Create points and segments ---
    points = np.array([data["x"], data["y"]]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if cRange is not None and norm is not None:
        raise ValueError("cRange and norm cannot both be specified")
    if cRange is not None:
        norm = plt.Normalize(cRange[0], cRange[1])
    lc = LineCollection(segments, cmap=cmap, norm=norm, **kwargs)

    # Set the values used for colormapping
    lc.set_array(data["c"])
    line = ax.add_collection(lc)
    if addColorBar:
        cBar = fig.colorbar(line, ax=ax)
        if cBarLabel is not None:
            cBar.set_label(cBarLabel)

    ax.autoscale()

    if returnFig:
        return fig, ax
    else:
        return


def All():
    """Runs commonly called functions provided in this module."""
    adjust_spines()
    draggable_legend()
    plt.gcf().canvas.mpl_connect("close_event", handle_close)
