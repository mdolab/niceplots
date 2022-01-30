"""
==============================================================================
Dark mode plotting example
==============================================================================
An example of dark mode usage applied to some of the existing examples. Shows
various usage of the dark_mode and set_dark_background in
niceplots.setRCParams().
"""

# ==============================================================================
# Standard Python modules
# ==============================================================================

# ==============================================================================
# External Python modules
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
import niceplots

# ==============================================================================
# Extension modules
# ==============================================================================

# Dark mode with a transparent background, saved to a png
niceplots.setRCParams(dark_mode=True)

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
c = np.cos(x)

fig, ax = plt.subplots()
niceplots.plotColoredLine(x, y, c, cmap="coolwarm", fig=fig, ax=ax, addColorBar=True, cRange=None, cBarLabel="$dy/dx$")
niceplots.plotColoredLine(x, c, -y, cmap="coolwarm", fig=fig, ax=ax, addColorBar=True, cRange=None, cBarLabel="$dy/dx$")
niceplots.adjust_spines(ax)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$", rotation="horizontal", ha="right")
ax.set_xticks(np.linspace(0, 2, 5) * np.pi)
ax.set_xticklabels([0, r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"])
ax.set_xlim(0, 2 * np.pi)
fig.savefig("coloredLine_dark.png", transparent=True, dpi=400)


# Plot contours with the default and a custom background color
niceColors = niceplots.get_niceColors()

bkgnd = [True, niceColors["Grey"], "#0c1c38"]  # different ways of setting the background via set_dark_background
fname_suffix = ["_dark", "_grey", "_navy"]

for i, back in enumerate(bkgnd):
    niceplots.setRCParams(dark_mode=True, set_dark_background=back)

    def f(x1, x2):
        return x1 ** 3 + 2.0 * x1 * x2 ** 2 - x2 ** 3 - 20.0 * x1

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
        color="w",
        markeredgecolor=q2ax.get_facecolor(),
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
        color="w",
        markeredgecolor=q2ax.get_facecolor(),
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
    )
    niceplots.adjust_spines(q2ax, outward=True)
    q2ax.set_xlabel("$x_1$")
    q2ax.set_xticks([min(x1), -minimum[0], 0, minimum[0], max(x1)])
    q2ax.set_xlim(left=min(x1), right=max(x1))
    q2ax.set_ylim(bottom=min(x2), top=max(x2))
    q2ax.set_yticks([min(x2), 0, minimum[-1], max(x2)])
    q2ax.set_ylabel("$x_2$", rotation="horizontal", ha="right")
    plt.savefig(f"ParulaContours{fname_suffix[i]}.png", dpi=400)
