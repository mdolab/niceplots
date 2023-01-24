"""
Bar chart
=========
An example of a bar chart.
"""
import matplotlib.pyplot as plt
import niceplots


header = ["Method", "Time (sec)"]
labels = [
    "Analytic Forward",
    "Analytic Adjoint",
    "FD Forward Diff.",
    "FD Central Diff.",
    "FD Backward Diff.",
]
times = [0.00456, 0.00847, 0.0110, 0.0213, 0.011]
nd = 4

with plt.style.context(niceplots.get_style()):
    niceplots.horiz_bar(labels, times, header, nd=nd, size=[7, 0.65])

    plt.savefig("bar_chart.png")
    plt.savefig("bar_chart.svg")
