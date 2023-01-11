"""
Plotting optimization problem
=============================
An example of how to use the :func:`niceplots.utils.plotOptProb` function to plot a constrained 2D optimization problem.
This example plots the 2D Rosenbrock function with a quadratic equality constraint and 3 circular inequality
constraints, which has an optimum at (1, 1).
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

niceplots.setStyle()


def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


def circleCon1(x, y):
    return x**2 + y**2 - 2


def circleCon2(x, y):
    return (x - 1.5) ** 2 + y**2 - 2


def circleCon3(x, y):
    return x**2 + (y - 1.5) ** 2 - 2


def eqCon(x, y):
    return x - y**2


# --- Some fake optimiser path ---
optX = [0.8, 1.2, 1.015384614926278, 0.9999252638670815, 1.0]
optY = [1.4, 1.3, 1.0626373624736707, 0.9999644713547426, 1.0]

for conStyle in ["shaded", "hashed"]:
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    niceplots.plotOptProb(
        Rosenbrock,
        xRange=[0, 1.5],
        yRange=[0, 1.5],
        ineqCon=[circleCon1, circleCon2, circleCon3],
        eqCon=eqCon,
        nPoints=31,
        optPoint=[1.0, 1.0],
        conStyle=conStyle,
        ax=ax,
        colors=None,
        cmap=None,
        levels=50,
        labelAxes=True,
    )

    # --- Plot the optimiser's path to the optimum ---
    ax.plot(
        optX,
        optY,
        "-o",
        c="#5a5758",
        markeredgecolor="w",
        linewidth=2.0,
        markersize=8,
        clip_on=False,
    )

    # Save figures
    fig.savefig(f"optProb-{conStyle}.png", dpi=400)
    fig.savefig(f"optProb-{conStyle}.pdf")
plt.show()
