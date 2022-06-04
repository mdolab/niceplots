"""
Nested pie chart
================
An example of a nested pie chart.
"""
import matplotlib.pyplot as plt
from niceplots import setRCParams, plotNestedPie

setRCParams()

data = {
    "Pie": {
        "Lime": 5,
        "Apple": 8,
        "Cow": 3,
    },
    "Not pie": {
        "Taco": 5,
        "Soup": 4,
    },
    "Pizza": {
        "Plain": 14,
        "White": 5,
        "Veggie": 12,
    },
}

# Custom colors
colors = ["#e86492", "#f0a43a", "#56b2f0"]

fig, ax = plt.subplots(figsize=(13, 8))
plotNestedPie(data, colors=colors, fig=fig, ax=ax)
ax.set_title("The best pies")

plt.savefig("nested_pie_chart.pdf", bbox_inches="tight")
plt.savefig("nested_pie_chart.png", dpi=400, bbox_inches="tight")
