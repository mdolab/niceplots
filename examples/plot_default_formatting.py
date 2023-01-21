"""
==============================================================================
Doumont Style Test
==============================================================================
@File    :   DoumontTest.py
@Date    :   2023/01/20
@Author  :   Alasdair Christison Gray
@Description :
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

xLine = np.linspace(xMin, xMax, 1000)
xRand = np.random.uniform(xMin, xMax, 45)
yLine = gaussian(xLine, 0, 1)
yRand = gaussian(xRand, 0, 1) + np.random.normal(0, 0.02, len(xRand))
yRand[yRand < 0] += 0.05

for formatting in ["default"] + niceplots.get_available_styles():
    with plt.style.context(niceplots.get_style(formatting)):

        if formatting != "default":
            colours = niceplots.get_colors()

        fig, ax = plt.subplots()

        ax.set_yticks([0, 0.4])
        ax.set_ylim(bottom=0, top=0.4)
        ax.set_xticks([xMin,-1, 0, 1,xMax])

        ax.set_xlabel("Some variable, $x$")
        ax.set_ylabel("$\\mathbb{E}(x,\\mu=0, \\sigma=1)$", rotation="horizontal", ha="right")

        line, = plt.plot(xLine, yLine, clip_on=False)
        markers, = plt.plot(xRand, yRand, "o", clip_on=False)

        ax.annotate("Calculated", xy=(-1.2, 0.2), ha="right", va="bottom", color=line.get_color())
        ax.annotate("Measured", xy=(0.7, 0.395), ha="left", va="top", color=markers.get_color())

        if formatting == "default":
            fill_color = "gray"
        else:
            fill_color = colours["Axis"]
        ax.fill_between(xLine, yLine, 0, where=np.abs(xLine)<=1, facecolor=fill_color, alpha=0.2, zorder=0)
        ax.annotate("68.27%", xy=(0,0.075), ha="center", va="bottom", color=fill_color)
        plt.annotate('', xy=(-1, 0.07), xytext=(1.0, 0.07),
            arrowprops=dict(arrowstyle='<|-|>', color=fill_color))

        if formatting != "default":
            niceplots.adjust_spines(ax)
        else:
            plt.tight_layout()
        fig.savefig(f"{formatting}-Gaussian.pdf")
        fig.savefig(f"{formatting}-Gaussian.png")
