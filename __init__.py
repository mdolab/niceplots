def adjust_spines(ax, spines=['left', 'bottom'], off_spines=['top', 'right']):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 18))  # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])

    for spine in off_spines:
        ax.spines[spine].set_visible(False)