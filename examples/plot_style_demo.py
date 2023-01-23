"""
==============================================================================
Niceplots Style Demo
==============================================================================
This script demonstrates the styles available in niceplots and compares them
to the default matplotlib style. The script generates a plot ofa Gaussian
distributions with some random "measured" data points and a shaded area
indicating a +/- 1 std dev region. The plot is loosely based on the plot shown
on page 147 of Jean Luc Doumont's "Trees, maps, and theorems" book.
"""

# ==============================================================================
# Standard Python modules
# ==============================================================================

# ==============================================================================
# External Python modules
# ==============================================================================
import matplotlib.pyplot as plt
import niceplots
import numpy as np

# ==============================================================================
# Extension modules
# ==============================================================================


def gaussian(x, mu, sig):
    return 1.0 / (np.sqrt(2.0 * np.pi) * sig) * np.exp(-np.power((x - mu) / sig, 2.0) / 2)


np.random.seed(0)

xMin = -3
xMax = 3

# Generate analytic gaussian distribution
xLine = np.linspace(xMin, xMax, 1000)
yLine = gaussian(xLine, 0, 1)

# Generate some fake "measured" data points with some noise
xRand = np.random.uniform(xMin, xMax, 45)
yRand = gaussian(xRand, 0, 1) + np.random.normal(0, 0.02, len(xRand))
yRand[yRand < 0] += 0.05

# Create a version of the plot with each niceplots style and the default matplotlib style
for formatting in ["default"] + niceplots.get_available_styles():
    with plt.style.context(niceplots.get_style(formatting)):

        # If using a niceplots style, we can get a nice dictionary of the style's colors
        if formatting != "default":
            colours = niceplots.get_colors()

        fig, ax = plt.subplots()

        # Plotting tip #1, only add axis ticks at important values
        ax.set_yticks([0, 0.4])
        ax.set_ylim(bottom=0, top=0.4)
        ax.set_xticks([xMin, -1, 0, 1, xMax])

        # Test out some LaTeX in the axis labels
        ax.set_xlabel("Some variable, $x$")
        ax.set_ylabel("$\\mathbb{E}(x,\\mu=0, \\sigma=1)$", rotation="horizontal", ha="right")

        # Plot the analytic and measured data, store the returned objects so we can get their colours later
        (line,) = plt.plot(xLine, yLine, clip_on=False)
        (markers,) = plt.plot(xRand, yRand, "o", clip_on=False)

        # Plotting tip #2, instead of a legend, put colored labels directly next to the data
        ax.annotate("Calculated", xy=(-1.2, 0.2), ha="right", va="bottom", color=line.get_color())
        ax.annotate("Measured", xy=(0.7, 0.395), ha="left", va="top", color=markers.get_color())

        # Plot the shaded area indicating the +/- 1 std dev region.
        # If using a niceplots style, we can use the colours dictionary to make the region the same color as the axes,
        # otherwise we'll just use gray
        if formatting == "default":
            fill_color = "gray"
        else:
            fill_color = colours["Axis"]

        ax.fill_between(xLine, yLine, 0, where=np.abs(xLine) <= 1, facecolor=fill_color, alpha=0.2, zorder=0)
        ax.annotate("68.27%", xy=(0, 0.075), ha="center", va="bottom", color=fill_color)
        plt.annotate("", xy=(-1, 0.07), xytext=(1.0, 0.07), arrowprops=dict(arrowstyle="<|-|>", color=fill_color))

        # Plotting tip #3, use the niceplots adjust_spines function to space the axes out nicely
        if formatting != "default":
            niceplots.adjust_spines(ax)
        else:
            plt.tight_layout()

        fig.savefig(f"{formatting}-Gaussian.pdf")
        fig.savefig(f"{formatting}-Gaussian.png")
