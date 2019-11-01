import numpy as np
import matplotlib.pyplot as plt
from niceplots import stacked_plots


# Set the random seed to get consistent results.
np.random.seed(314)

# Create some fake data to plot.
# Time will be the x-axis, altitude and Mach will be two plots stacked on top of each other for the y-axes.
nn = 50
time = np.linspace(0, 250, nn)
altitude = np.linspace(0, 35000, nn) + np.random.random_sample(nn) * 10000
mach = np.linspace(0.2, 1., nn)**2 + np.random.random_sample(nn) * 0.2

# Create a dictionary to store the data from above.
# The keys will be the labels on the y-axes and the data will be plotted.
data_to_plot = {}
data_to_plot['Altitude, ft'] = altitude
data_to_plot['Mach'] = mach

# Call the stacked_plots function with the data we created.
# Give the x-axis label and data first, then the dictionary containing all
# y-axes information.
# You can set some plot options here as well, like the pad distance for the
# y-labels from the y-axes if you have long labels.
# This function will save a pdf with the filename given.
stacked_plots('Time, secs', time, data_to_plot, pad=100, figsize=(10, 6), filename='opt_stacks.pdf')

# Create second set of data to plot to show other options for stacked_plots.
altitude = np.linspace(35000, 0., nn) + np.random.random_sample(nn) * 10000
mach = np.linspace(1, 0.5, nn)**2 + np.random.random_sample(nn) * 0.2
data_to_plot_2 = {}
data_to_plot_2['Altitude, ft'] = altitude
data_to_plot_2['Mach'] = mach

# stacked_plots can also accept a list of dicts to plot multiple strains
# of data on the same set of plots.
# We grabbed the fig and axarr handles here so that we can modify the plot.
f, axarr = stacked_plots('Time, secs', time, [data_to_plot, data_to_plot_2], pad=100, figsize=(10, 6), filename='opt_stacks_more_data.pdf')

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

# Save out another version of the figure, this time with our labels added.
plt.savefig('opt_stacks_with_labels.pdf', bbox_inches='tight')
