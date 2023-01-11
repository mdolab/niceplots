"""
Default formatting
==================
A short example to demonstrate the use of niceplots default plot formatting and compre it to matplotlib defaults
"""

import numpy as np
import matplotlib.pyplot as plt
import niceplots


# This function computes the displacement history of an undamped oscilator subjec to to a force pulse of length tp
def MSPulseResponse(t, tp, omega):
    x = np.where(
        t < tp,
        1.0 - np.cos(omega * t),
        (np.cos(omega * tp) - 1.0) * np.cos(omega * t) + np.sin(omega * tp) * np.sin(omega * t),
    )
    return x


m = 1.0
k = 100.0
omega = np.sqrt(k / m)
t = np.linspace(0, 3.0, 1001)
TP = [0.5, 0.8, 1.2, 1.6, 2.0]

for formatting in ["default"] + niceplots.get_available_styles():
    if formatting != "default":
        niceplots.setStyle(formatting, afterReset=True)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    fig, axes = plt.subplots(nrows=len(TP), figsize=(12, 16))

    for i in range(len(TP)):
        tp = TP[i]
        ax = axes[i]
        x = MSPulseResponse(t, tp, omega)
        line = ax.plot(t, x, clip_on=False, color=colors[i])
        ax.vlines(tp, -3, 1.0 - np.cos(omega * tp), linestyle="--", color="gray", zorder=0)
        ax.set_xticks([0, tp, 3])
        if i == len(TP) - 1:
            ax.set_xlabel("t (s)")
        ax.set_ylabel(r"$\frac{x(t)}{x_s}$", ha="right", rotation="horizontal")
        ax.set_ylim(bottom=-2.0, top=2.0)
        if formatting != "default":
            niceplots.adjust_spines(ax, outward=True)

    plt.savefig(f"{formatting}PulseResponse.pdf")
    plt.savefig(f"{formatting}PulseResponse.png", dpi=400)
