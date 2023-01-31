import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from .parula import parula_map
from matplotlib import patheffects
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolor
import warnings
import os


def get_style(styleName="doumont-light"):
    """
    Get the stylesheet to pass to matplotlib's style setting functions. This function
    works both with niceplots styles and matplotlib's built-in styles. Usage examples::

        import matplotlib.pyplot as plt
        import niceplots

        plt.style.use(niceplots.get_style())
        plt.plot([0, 1], [0, 1])

        # Or you can use it within a context manager
        with plt.style.context(niceplots.get_style()):
            plt.plot([0, 1], [0, 1])

        # Also try different styles
        plt.style.use(niceplots.get_style("james-dark"))  # niceplots james dark style
        plt.style.use(niceplots.get_style("default"))  # matplotlib default style

    Parameters
    ----------
    styleName : str, optional
        Name of desired style. By default uses doumont-light style. Avaiable styles are:

            - doumont-light: the niceplots style you know and love
            - doumont-dark: the dark version of the niceplots style you know and love
            - james-dark: a really cool alternative to classic niceplots
            - james-light: a version of james with a light background, naturally

    Returns
    -------
    str
        The style string to be passed to one of matplotlib's style setting functions.
    """
    # If the style is a niceplots style, return the file path
    if styleName in get_available_styles():
        curDir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(curDir, "styles", styleName + ".mplstyle")

    # Otherwise assume it's a matplotlib style and just return the style name
    return styleName


def get_colors():
    """
    Get a dictionary with the colors for the current style. This function
    only works when niceplots styles are used (not built-in matplotlib ones).

    Returns
    -------
    dict
        Dictionary of the colors for the requested style. The keys
        are human-readable names and the keys are the hex codes. It
        also adds color names from the rcParams that are generally useful:

            - "Axis": axis spine color
            - "Background" axis background color
            - "Text": default text color
            - "Label": axis label color
    """
    # Get the color codes and their names from the (hopefully) "special" parameter
    color_codes = get_colors_list()
    color_names = plt.rcParams["keymap.help"]

    # Ensure that the amount of color names matches the amount of colors
    if len(color_codes) != len(color_names):
        raise ValueError(
            "The colors are not properly named in the stylesheet, please open an issue on GitHub with the details!"
        )

    colors = OrderedDict(zip(color_names, color_codes))
    colors["Axis"] = plt.rcParams["axes.edgecolor"]
    colors["Background"] = plt.rcParams["axes.facecolor"]
    colors["Text"] = plt.rcParams["text.color"]
    colors["Label"] = plt.rcParams["axes.labelcolor"]

    return colors


def get_colors_list():
    """
    Get a list with the colors for the current style. This function
    works with all matplotlib styles.

    Returns
    -------
    list
        List of the colors for the requested style.
    """
    return plt.rcParams["axes.prop_cycle"].by_key()["color"]


def get_available_styles():
    """
    Get a list of the names of styles available.

    Returns
    -------
    list
        The names of the available styles.
    """
    curDir = os.path.dirname(os.path.abspath(__file__))
    styleFilenames = os.listdir(os.path.join(curDir, "styles"))
    styles = []
    for s in styleFilenames:
        name, ext = os.path.splitext(s)
        if ext == ".mplstyle":
            styles.append(name)
    styles.sort()  # alphabetize
    return styles


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


def draggable_legend(axis=None, color_on=True, **kwargs):
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
        legend.append(axis.annotate(label, xy=coords, color=color, xycoords="axes fraction", **kwargs))
        legend[idx].draggable()


def label_line_ends(ax, lines=None, labels=None, colors=None, x_offset_pts=6, y_offset_pts=0, **kwargs):
    """Place a label just to the right of each line in the axes

    Note: Because the labels are placed outside of the axes, this function works best for plots where all lines end as
    close to the right edge of the axes as possible. Additionally you need to either use constrained_layout=True
    (as NicePlots styles do), or call plt.tight_layout() after calling this function.

    Parameters
    ----------
    ax : Matplotlib axes
        axes to label the lines of
    lines : iterable of matplotlib line objects, optional
        Lines to label, by default all lines in the axes
    labels : list of strings, optional
        Labels for each line, by default uses each line's label attribute
    colors : single or list of colors, optional
        Color(s) to use for each line, can be a single color for all lines or a list containing an entry for each line,
        by default uses each line's color
    x_offset_pts : int, float, optional
        Horizontal offset of label from the right end of the line, in points, by default 6
    y_offset_pts : int, float, optional
        Vertical offset of label from the right end of the line, in points, by default 0
    **kwargs :
        Any valid keywords for matplotlib's annotate function, except ``xy``, ``xytext``, ``color``, ``textcoords``,
        ``va``

    Returns
    -------
    list of matplotlib annotation objects
        The annotations created
    """
    if lines is None:
        lines = ax.get_lines()

    if labels is None:
        labels = [line.get_label() for line in lines]
    numLines = len(lines)
    if len(labels) != numLines:
        raise ValueError(f"Number of labels ({len(labels)}) doesn't match number of lines ({numLines})")

    if colors is None:
        colors = [line.get_color() for line in lines]
    if not isinstance(colors, list):
        colors = [colors] * len(lines)
    if len(colors) != numLines:
        raise ValueError(f"Number of colors ({len(colors)}) doesn't match number of lines ({numLines})")

    annotations = []

    for line, label, color in zip(lines, labels, colors):
        # Get the x, y coordinates of the right-most point on the line
        maxXIndex = np.argmax(line.get_xdata())
        x = line.get_xdata()[maxXIndex]
        y = line.get_ydata()[maxXIndex]
        annote = ax.annotate(
            label,
            xy=(x, y),
            xytext=(x_offset_pts, y_offset_pts),
            color=color,
            textcoords="offset points",
            va="center",
            **kwargs,
        )
        annotations.append(annote)

    return annotations


def horiz_bar(labels, times, header, nd=1, size=[5, 0.5], color=None):
    """Creates a horizontal bar chart to compare positive numbers.

    Parameters
    ----------
    labels : list of str
        contains the ordered labels for each data set
    times : list of float
        contains the numerical data for each entry
    header : list of two str
        contains the left and right header for the labels and
        numeric data, respectively
    nd : float
        the number of digits to show after the decimal point for the data
    size : list of two float
        the size of the final figure (iffy results)
    color : str
        hexcode for the color of the scatter points used

    Returns
    -------
    fig: matplotlib Figure
        Figure created
    ax: matplotlib Axes
        Axes on which data is plotted
    """

    # Use the first color if none is specified
    if color is None:
        color = get_colors_list()[0]
    style_colors = get_colors()
    line_color = style_colors["Axis"]

    # Obtain parameters to size the chart correctly
    num = len(times)
    width = size[0]
    height = size[1] * num
    t_max = max(times)

    # Create the corresponding number of subplots for each individual timing
    fig, axarr = plt.subplots(num, 1, figsize=[width, height])

    # Loop over each time and get the max number of digits
    t_max_digits = 0
    for t in times:
        tm = len(str(int(t)))
        if tm > t_max_digits:
            t_max_digits = tm

    # Actual loop that draws each bar
    for j, (l, t, ax) in enumerate(zip(labels, times, axarr)):

        # Draw the gray line and singular yellow dot
        ax.axhline(y=1, c=line_color, lw=3, zorder=0, alpha=0.5)
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
        ax.set_ylabel(l, rotation="horizontal", ha="right", va="center")
        string = "{number:.{digits}f}".format(number=t, digits=nd)
        ax.annotate(
            string, xy=(1, 1), xytext=(6, 0), xycoords=ax.get_yaxis_transform(), textcoords="offset points", va="center"
        )

        # Create the top bar line
        if j == 0:
            ax.text(0, 1.02, header[0], ha="right", fontweight="bold", fontsize="large")
            ax.text(t_max, 1.02, header[1], ha="left", fontweight="bold", fontsize="large")

    return fig, ax


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
        colors = get_colors_list()

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


def plot_opt_prob(
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
        colors = get_colors_list()
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


def plot_colored_line(
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


def plot_nested_pie(
    data,
    colors=None,
    alphas=None,
    ax=None,
    innerKwargs=None,
    outerKwargs=None,
):
    """Create a two-level pie chart where the inner pie chart is a sum of related categories from the outer one.
    The labels are by default set to the keys in the data dictionary.

    Parameters
    ----------
    data : nested dict
        Data to plot. Formatted as::

            {
                "Category 1": {
                    "Subcategory 1": 0.5,
                    "Subcategory 2": 1.5,
                },
                "Category 2": {
                    "Subcategory 1": 2.5,
                },
                ...
            }

    colors : str or list of str with hex colors, optional
        Colors to use for the inner wedges. Can either specify a qualitative matplotlib colormap (it will assume
        this is the case if a string is specified), or a list of colors specified with hex codes (e.g., "#F4A103"),
        by default will use nice colors (niceplots default). Loops through the colors if more categories than
        colors are specified.
    alphas : iterable of floats at least as long as the max number of subcategories for a given category
        Transparencies to use to vary the color in the outer categories
    ax : matplotlib axes object, optional
        axes to plot on, by default None, in which case a new figure will be created and returned by the function
    innerKwargs : dict
        Dictionary of keyword arguments to pass to matplotlib.pyplot.pie for the inner pie chart. "color" and "radius"
        are important ones for the nested pie chart and I recommend not touching those unless you know what you're
        doing. labels, rotatelabels, wedgeprops, and textprops are also all set by default in this function, but
        can be overridden using this parameter
    outerKwargs : dict
        Dictionary of keyword arguments to pass to matplotlib.pyplot.pie for the outer pie chart. "color" and "radius"
        are important ones for the nested pie chart and I recommend not touching those unless you know what you're
        doing. labels, rotatelabels, wedgeprops, and textprops are also all set by default in this function, but
        can be overridden using this parameter

    Returns
    -------
    pieObjects : dict of matplotlib.patches.Wedge and matplotlib Text objects
        Wedges and text objects for the pie plot, formatted similarly to the input data dict::

            {
                "Category 1": {
                    "wedge": Category 1 wedge
                    "text": Category 1 text
                    "Subcategory 1": {"wedge": Subcategory 1 wedge, "text": Subcategory 1 wedge},
                    "Subcategory 2": {"wedge": Subcategory 2 wedge, "text": Subcategory 2 wedge},
                },
                "Category 2": {
                    "wedge": Category 2 wedge
                    "text": Category 2 text
                    "Subcategory 1": {"wedge": Subcategory 1 wedge, "text": Subcategory 1 wedge},
                },
                ...
            }

    fig : matplotlib figure object
        Figure containing the plot. Returned only if no input ax object is specified
    ax : matplotlib axes object
        Axis with the colored line. Returned only if no input ax object is specified
    """
    # If colors is not specified, turn the style's colors into a list of hex colors
    if colors is None:
        colors = [c for c in get_colors().values()]
    # If colors is given as a qualitative matplotlib colormap, turn it into a list of hex colors
    elif isinstance(colors, str):
        colors = [mcolor.rgb2hex(plt.colormaps[colors](i)) for i in range(len(data))]
    numColors = len(colors)

    # Go through the colors and only take the color information (not transparency)
    for i in range(len(colors)):
        if colors[i][0] != "#":
            raise ValueError("Colors specified as a string must start with a #")
        colors[i] = colors[i][0:7]

    # Sum categories and collapse subcategories
    innerVals = []
    innerLabels = []
    outerVals = []
    outerLabels = []
    total = 0.0
    maxSubcat = 0.0
    for cat, val in data.items():  # top level categories
        innerLabels.append(cat)
        innerVals.append(0.0)

        # Max number of subcategories for a given category
        maxSubcat = max(maxSubcat, len(val))

        for subcat, subcatVal in val.items():
            innerVals[-1] += subcatVal
            total += subcatVal

            outerVals.append(subcatVal)
            outerLabels.append(subcat)

    # Define alphas if not specified
    if alphas is None:
        alphas = np.linspace(0.75, 0.95, maxSubcat)[-1::-1]

    innerColors = [colors[i % numColors] for i in range(len(data))]
    outerColors = []
    iCat = 0
    for catVals in data.values():
        numSubcats = len(catVals)
        for iSubcat in range(numSubcats):
            outerColors.append(colors[iCat % numColors] + float.hex(alphas[iSubcat])[4:6])
        iCat += 1

    # Nested plot fitting params
    size = 0.3
    buffer = 0.01

    # Create figure if it's not passed in
    returnFig = False
    if ax is None:
        fig, ax = plt.subplots()
        returnFig = True

    # Set keyword arguments
    outerKwargDefaults = {
        "radius": 1.0,
        "colors": outerColors,
        "wedgeprops": dict(width=size, edgecolor=None),
        "textprops": dict(rotation_mode="anchor", va="center", ha="center", color="w"),
        "labels": outerLabels,
        "rotatelabels": False,
        "labeldistance": 0.85,
    }
    innerKwargDefaults = {
        "radius": 1.0 - size - buffer,
        "colors": innerColors,
        "wedgeprops": dict(width=size, edgecolor=None),
        "textprops": dict(rotation_mode="anchor", va="center", ha="center", color="w"),
        "labels": innerLabels,
        "rotatelabels": False,
        "labeldistance": 0.75,
    }
    outerKwargs = {} if outerKwargs is None else outerKwargs
    innerKwargs = {} if innerKwargs is None else innerKwargs

    # Update kwargs
    for outerKey, outerKwargVal in outerKwargDefaults.items():
        if outerKey not in outerKwargs:
            outerKwargs[outerKey] = outerKwargVal
    for innerKey, innerKwargVal in innerKwargDefaults.items():
        if innerKey not in innerKwargs:
            innerKwargs[innerKey] = innerKwargVal

    # Create the pie charts
    outerWedges, outerText = ax.pie(outerVals, **outerKwargs)
    innerWedges, innerText = ax.pie(innerVals, **innerKwargs)

    ax.set(aspect="equal")

    # Compile the wedge and text objects into the output dictionary
    pieObjects = {}
    iSubcat = 0
    for i, cat in enumerate(data.keys()):
        pieObjects[cat] = {
            "wedge": innerWedges[i],
            "text": innerText[i],
        }

        for subcat in data[cat].keys():
            pieObjects[cat][subcat] = {
                "wedge": outerWedges[iSubcat],
                "text": outerText[iSubcat],
            }
            iSubcat += 1

    if returnFig:
        return pieObjects, fig, ax
    else:
        return pieObjects


def All():
    """Runs commonly called functions provided in this module."""
    adjust_spines()
    draggable_legend()
    plt.gcf().canvas.mpl_connect("close_event", handle_close)
