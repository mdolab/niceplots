"""
==============================================================================
NicePlots Style Colors Demo
==============================================================================
This script demonstrates colors available in each style.
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

# Get the style names from NicePlots
styles = niceplots.get_available_styles()

plt.style.use(niceplots.get_style("james-light"))

fig, axs = plt.subplots(1, len(styles), figsize=(3 * len(styles), 8))
axs = axs.flatten()

for i, style in enumerate(styles):
    with plt.style.context(niceplots.get_style(style)):
        ax = axs[i]
        colors = niceplots.get_colors()
        background = colors["Background"]
        for key in ["Axis", "Background", "Text", "Label"]:
            del colors[key]

        ax.set_title(style, pad=20.0)

        # Fill the background with the style's background color
        ax.fill_between([0, 1], [0, 0], [1, 1], color=background)

        # Swatch properties
        spacing = 0.05
        y_spacing = spacing * 3
        width = (1 - (len(colors) + 1) * spacing) / len(colors)

        # Plot the swatches
        for i_color, color in enumerate(colors.keys()):
            y_start = i_color * (spacing + width) + spacing
            y_end = width + y_start
            ax.fill_between([y_spacing, 1 - y_spacing], [y_start] * 2, [y_end] * 2, color=colors[color])
            ax.text(0.5, (y_start + y_end) / 2, color, va="center", ha="center")

        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.invert_yaxis()

        # Remove the spines and ticks
        ax.spines[["top", "bottom", "left", "right"]].set_visible(False)
        ax.set_xticks(())
        ax.set_yticks(())

fig.savefig("style_color_demo.png")
fig.savefig("style_color_demo.svg")
