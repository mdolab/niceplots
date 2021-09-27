"""
==============================================================================
Optimization problem plotting example
==============================================================================
@File    :   optProb.py
@Date    :   2021/09/27
@Author  :   Alasdair Christison Gray
@Description : An example of how to use the plotOptProb function to plot a constrained 2D optimization problem.
In this example I plot the 2D rosenbrock function with an equlity constraint and an inequality constraint.
"""

# ==============================================================================
# Standard Python modules
# ==============================================================================

# ==============================================================================
# External Python modules
# ==============================================================================
import matplotlib.pyplot as plt
import niceplots


# ==============================================================================
# Extension modules
# ==============================================================================

niceplots.setRCParams()
niceColors = niceplots.get_niceColors()


def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def circleCon(x, y):
    return x ** 2 + y ** 2 - 2


def linCon(x, y):
    return x - y


fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")
ax = niceplots.plotOptProb(
    Rosenbrock,
    xRange=[-1.5, 1.5],
    yRange=[-1.5, 1.5],
    ineqCon=circleCon,
    eqCon=linCon,
    nPoints=51,
    optPoint=[1.0, 1.0],
    conStyle="shaded",
    ax=ax,
    colors=None,
    cmap=None,
    levels=50,
    labelAxes=True,
)
fig.savefig("optProb.png", dpi=400)
fig.savefig("optProb.pdf")
plt.show()
