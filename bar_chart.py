from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import random

def align_decimal(number, left_pad=7, precision=2):
    """Format a number in a way that will align decimal points."""
    outer = '{0:>%i}.{1:<%i}' % (left_pad, precision)
    inner = '{:.%if}' % (precision,)
    return outer.format(*(inner.format(number).split('.')))

def horiz_bar(labels, times, header, ts=1, nd=1, size=[5, .5], color='#FFCC00'):
    num = len(times)
    size[1] = size[1] * num
    t_max = max(times)
    l_max = len(max(labels, key=len))

    fig, axarr = plt.subplots(num, 1)

    # playing with these values here can help with label alignment
    left_lim = -ts*l_max*.038*t_max
    right_lim = t_max*1.11

    # these values tweak the header label placement
    left_header_pos = -len(header[0])*.018*t_max + left_lim/2
    right_header_pos = -len(header[1])*.018*t_max + right_lim + t_max*(.09+nd*.02)

    t_max_digits = 0
    for t in times:
        tm = len(str(int(t)))
        if tm > t_max_digits:
            t_max_digits = tm

    for j,(l,t,ax) in enumerate(zip(labels, times, axarr)): 

        ax.axhline(y=1, c='#C0C0C0', lw=3, zorder=0)
        ax.scatter([t],[1], c=color, lw=0, s=100, zorder=1, clip_on=False)
        ax.set_ylim(.99, 1.01)
        ax.set_xlim(0, t_max*1.05)
        ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,      # ticks along the bottom edge are off
            labelleft=False, 
            labelright=False,
            labelbottom=False, 
            right=False,         # ticks along the top edge are off
            bottom=j==num, 
            top=False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.text(left_lim, .997, l)
        d = t_max_digits - len(str(int(t)))
        eval("ax.text(right_lim, .997, '  ' * d + '%0.{}f'%t)".format(nd))

        if j == 0: 
            ax.text(left_header_pos,1.02, header[0], fontsize=13)
            ax.text(right_header_pos,1.02, header[1], fontsize=13)
            
            line = Line2D([left_lim, right_lim+t_max*(.15+nd*.02)], [1.012, 1.012], lw=1.2, color='k')
            line.set_clip_on(False)
            ax.add_line(line)

            line = Line2D([left_lim, right_lim+t_max*(.15+nd*.02)], [1.01, 1.01], lw=1.2, color='k')
            line.set_clip_on(False)
            ax.add_line(line)
    fig.set_size_inches(size[0], size[1])
    fig.savefig('bar_chart.pdf', bbox_inches="tight")