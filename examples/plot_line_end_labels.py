"""
==============================================================================
Line end labelling
==============================================================================
An example demonstrating the use of label_line_ends to
automatically label the ends of lines nicely.
"""

# ==============================================================================
# External Python modules
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
import niceplots


def plot_colored_lines(ax, n_lines=3):
    """Plot lines with colors following the style color cycle.

    Adapted from https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
    """
    t = np.linspace(-10, 20, 100)

    def sigmoid(t, t0):
        return 1 / (1 + np.exp(-(t - t0)))

    shifts = np.linspace(0, 10, n_lines)
    amplitudes = np.linspace(1, 1.5, n_lines)
    for t0, a in zip(shifts, amplitudes):
        ax.plot(t, a * sigmoid(t, t0), "-", label=f"$t_0={t0}$", clip_on=False)
    ax.set_xlim(-10, 20)


plt.style.use(niceplots.get_style())

fig, ax = plt.subplots()
plot_colored_lines(ax)
ax.set_xlabel("t")
ax.set_ylabel("$\sigma$", rotation="horizontal", ha="right")
niceplots.adjust_spines(ax)
niceplots.label_line_ends(ax)

niceplots.save_figs(fig, "line_end_labels", ["png", "svg"])
