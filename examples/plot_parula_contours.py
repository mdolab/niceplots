"""
Parula colormap example
=======================
Demonstrate niceplot's Parula colormap on a simple contour plot
"""

# ==============================================================================
# Standard Python modules
# ==============================================================================

# ==============================================================================
# External Python modules
# ==============================================================================
import numpy as np
from matplotlib import pyplot as plt
import niceplots


niceplots.setRCParams()
niceColors = niceplots.get_niceColors()


def f(x1, x2):
    return x1**3 + 2.0 * x1 * x2**2 - x2**3 - 20.0 * x1


x1 = x2 = np.linspace(-5, 5, 201)
X1, X2 = np.meshgrid(x1, x2)
minimum = [2.58199, 0]

q2fig, q2ax = plt.subplots()
q2ax.contour(X1, X2, f(X1, X2), cmap=niceplots.parula.parula_map, levels=40)
q2ax.plot(
    minimum[0],
    minimum[1],
    clip_on=False,
    marker="o",
    color=niceColors["Grey"],
    markeredgecolor="w",
    linestyle="",
    markersize=12,
)
q2ax.annotate(
    "Local Minimum",
    xy=minimum,
    xytext=(-5, 10),
    textcoords="offset points",
    va="bottom",
    ha="center",
)
q2ax.plot(
    -minimum[0],
    minimum[1],
    clip_on=False,
    marker="o",
    color=niceColors["Grey"],
    markeredgecolor="w",
    linestyle="",
    markersize=12,
)
q2ax.annotate(
    "Local Maximum",
    xy=(-minimum[0], 0),
    xytext=(0, -10),
    textcoords="offset points",
    va="top",
    ha="center",
    color=niceColors["Grey"],
)
niceplots.adjust_spines(q2ax, outward=True)
q2ax.set_xlabel("$x_1$")
q2ax.set_xticks([min(x1), -minimum[0], 0, minimum[0], max(x1)])
q2ax.set_xlim(left=min(x1), right=max(x1))
q2ax.set_ylim(bottom=min(x2), top=max(x2))
q2ax.set_yticks([min(x2), 0, minimum[-1], max(x2)])
q2ax.set_ylabel("$x_2$", rotation="horizontal", ha="right")
plt.savefig("ParulaContours.png", dpi=400)
