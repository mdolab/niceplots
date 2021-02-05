import numpy as np
import matplotlib.pyplot as plt
import niceplots

niceplots.setRCParams()

# Set the random seed to get consistent results.
np.random.seed(314)

# Create some fake data to plot.
# Time will be the x-axis, position and velocity of a damped oscilator will be two plots stacked on top of each other
# for the y-axes.
nn = 30
n_lines = 4
phases = np.random.random_sample(n_lines) * 2.0 * np.pi
damping = -np.random.random_sample(n_lines) * 2.0 * 250.0
time = np.linspace(0, 250.0, nn)
data = []

for phase, damp in zip(phases, damping):
    Position = 1.0 + np.sin(2 * np.pi * time / 100 + phase) * np.exp(time / damp)
    Velocity = (
        2 * np.pi / 100 * np.cos(2 * np.pi * time / 100 + phase) * np.exp(time / damp)
    )

    data.append({})
    data[-1]["Position (m)"] = Position
    data[-1]["Velocity (m/s)"] = Velocity

# Call the stacked_plots function with the data we created.
# Give the x-axis label and data first, then the dictionary containing all
# y-axes information.
# You can set some plot options here as well, like the pad distance for the
# y-labels from the y-axes if you have long labels.
# This function will save a pdf with the filename given.
niceplots.stacked_plots(
    "Time (s)", time, data[0], figsize=(10, 6), filename="opt_stacks.pdf"
)
plt.savefig("opt_stacks.png", dpi=400)

# stacked_plots can also accept a list of dicts to plot multiple strains
# of data on the same set of plots.
# We grabbed the fig and axarr handles here so that we can modify the plot.
# Also, since there are many lines, we use the line_scaler option to reduce their thickness and keep the plot clean
f, axarr = niceplots.stacked_plots(
    "Time (s)",
    time,
    data,
    figsize=(10, 6),
    line_scaler=0.5,
    filename="opt_stacks_more_data.pdf",
)
plt.savefig("opt_stacks_more_data.png", dpi=400)
