import numpy as np
import matplotlib.pyplot as plt
import niceplots

niceplots.setRCParams()

# Set the random seed to get consistent results.
np.random.seed(314)

# Create some fake data to plot.
# Time will be the x-axis, altitude and Mach will be two plots stacked on top of each other for the y-axes.
nn = 50
n_lines = 8
phases = np.random.random_sample(n_lines)*2.0*np.pi
damping = -np.random.random_sample(n_lines)*250.0
time = np.linspace(0, 250., nn)
data = []

for phase, damp in zip(phases, damping):
    Position = 1.0 + np.sin(2*np.pi*time/100+phase)*np.exp(time/damp)
    Velocity = 2*np.pi/100*np.cos(2*np.pi*time/100+phase)*np.exp(time/damp)

    data.append({})
    data[-1]['Position (m)'] = Position
    data[-1]['Velocity (m/s)'] = Velocity

# Call the stacked_plots function with the data we created.
# Give the x-axis label and data first, then the dictionary containing all
# y-axes information.
# You can set some plot options here as well, like the pad distance for the
# y-labels from the y-axes if you have long labels.
# This function will save a pdf with the filename given.
niceplots.stacked_plots('Time, secs', time, data[0], pad=100, figsize=(10, 6), filename='opt_stacks.pdf')

# stacked_plots can also accept a list of dicts to plot multiple strains
# of data on the same set of plots.
# We grabbed the fig and axarr handles here so that we can modify the plot.
f, axarr = niceplots.stacked_plots('Time, secs', time, data, pad=100, figsize=(10, 6), filename='opt_stacks_more_data.pdf')

# Now we can customize the plot produced by stacked_plots. We could want to do
# this to add labels, notes, or plot our own data in special cases.
# Here we'll add some labels matching the colors in the plots.

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

ax = axarr[0]
anchor = 0.05
ax.annotate('Run 1', xy=(anchor, anchor + 0.1), xytext=(.65, .8), xycoords='axes fraction',
        rotation=0., color=colors[0])
ax.annotate('Run 2', xy=(anchor, anchor + 0.05), xytext=(anchor, anchor + 0.5), xycoords='axes fraction',
        rotation=0., color=colors[1])

# # Save out another version of the figure, this time with our labels added.
# plt.savefig('opt_stacks_with_labels.pdf', bbox_inches='tight')
