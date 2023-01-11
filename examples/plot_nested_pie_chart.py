"""
Nested pie chart
================
An example of a nested pie chart.
"""
import matplotlib.pyplot as plt
import niceplots

plt.style.use(niceplots.get_style("james-dark"))
colors = niceplots.get_colors()

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
        "Cheese": 14,
        "White": 5,
        "Veggie": 12,
    },
}

fig, ax = plt.subplots(figsize=(8, 8))
pieObjects = niceplots.plot_nested_pie(data, colors=list(colors.values()), ax=ax)

# Customize one of the wedges...
pieObjects["Pizza"]["Cheese"]["wedge"].set_radius(1.1)
pieObjects["Pizza"]["Cheese"]["wedge"].set_width(0.4)

# ...and its text
pieObjects["Pizza"]["Cheese"]["text"].set_weight("bold")
pieObjects["Pizza"]["Cheese"]["text"].set_x(-0.82)

plt.savefig("nested_pie_chart.pdf", bbox_inches="tight")
plt.savefig("nested_pie_chart.png", dpi=400, bbox_inches="tight")
