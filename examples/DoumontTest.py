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


plt.style.use(niceplots.get_style("doumont-light"))
colours = niceplots.get_colors()
np.random.seed(0)

fig, ax = plt.subplots()

xMin = -3
xMax = 3

xLine = np.linspace(xMin, xMax, 1000)
xRand = np.random.uniform(xMin, xMax, 45)
yLine = gaussian(xLine, 0, 1)
yRand = gaussian(xRand, 0, 1) + np.random.normal(0, 0.02, len(xRand))
yRand[yRand < 0] += 0.05

ax.set_yticks([0, 0.4])
ax.set_ylim(bottom=0, top=0.4)
ax.set_xticks([xMin, 0, xMax])

ax.set_xlabel("Some variable, $x$")
ax.set_ylabel("$\mathbb{E}(x,\\mu=0, \sigma=1)$", rotation="horizontal", ha="right")

ax.annotate("Calculated", xy=(-1.2, 0.2), ha="right", va="bottom", color=colours["Yellow"])
ax.annotate("Measured", xy=(0.7, 0.395), ha="left", va="top", color=colours["Blue"])

plt.plot(xLine, yLine, clip_on=False)
plt.plot(xRand, yRand, "o", clip_on=False)
niceplots.adjust_spines(ax)
plt.show()
