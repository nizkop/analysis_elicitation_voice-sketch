from src.color_codes import global_colors
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.ticker import FuncFormatter

# cite Norda_2024

level = [3,4,5,6,7,10]
time_equivalent = [1.38, 0.82, 0.40, 0.35]


interactions = [1,3,5,6,7,10]
time_equivalent = [1.38, 0.79, 0.48, 0.39, 0.33, 0.34]


import matplotlib.transforms as mtransforms

def set_one_label_upside(ax):
    ax.tick_params(axis='x', labelbottom=True, labeltop=False)
    ticks = ax.xaxis.get_major_ticks()
    labels = ax.get_xticklabels()

    idx = 0

    for i, tick in enumerate(ticks):
        if i == idx:
            tick.tick1line.set_visible(False)  # unten weg
            tick.tick2line.set_visible(True)  # oben an
            offset_transform = mtransforms.Affine2D().translate(0,-1.2) + ax.transData
            tick.tick2line.set_transform(offset_transform)
        else:
            tick.tick1line.set_visible(True)  # unten an
            tick.tick2line.set_visible(False)  # oben aus

    for i, label in enumerate(labels):
        if i == idx:
            label.set_visible(True)
            label.set_verticalalignment('bottom')
            label.set_y(5)
        else:
            label.set_visible(True)
            label.set_verticalalignment('top')
            label.set_y(-0.02)

# Geschweifte Klammer zeichnen
def get_geschweifte_klammer(y_min, y_max, x_pos, ax, text):
    """

    :param y_min:
    :param y_max:
    :param x_pos: Position der geschweiften Klammer auf der x-Achse (außerhalb des Plot-Bereichs); Position der Klammer links von der y-Achse
    :param ax:
    :param text:
    :return:
    """
    vertices = [
        (x_pos, y_min),
        (x_pos - 0.2, y_min),
        (x_pos - 0.2, (y_min + y_max) / 2),
        (x_pos - 0.3, (y_min + y_max) / 2),
        (x_pos - 0.2, (y_min + y_max) / 2),
        (x_pos - 0.2, y_max),
        (x_pos, y_max)
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO
    ]
    path = Path(vertices, codes)
    patch = PathPatch(path, facecolor='none', edgecolor='black', lw=2)
    ax.add_patch(patch)
    # Text neben der geschweiften Klammer
    return ax.text(x_pos - 0.4, (y_min + y_max) / 2, text, va='center', ha='right')


def get_percentage(time_equivalente: list):
    percentages = [100*(1-i) for i in time_equivalente]
    return percentages


y_values = get_percentage(time_equivalent)

fig, ax = my_plt.subplots(figsize=(figure_width, default_height-2))# 7,3
bars = ax.bar(interactions, y_values, color=global_colors[None])

# Bereich auf der y-Achse, der markiert werden soll
y_min = 0
y_max = max(y_values)



kl1 = get_geschweifte_klammer(y_min=0.5, y_max=max(y_values),x_pos=0.25, ax=ax, text='voice\ncontrol\nfaster')
kl2 = get_geschweifte_klammer(y_min=min(y_values), y_max=-0.5, x_pos=-0.1,ax=ax, text='touch\ninput\nfaster')


# x-Bereich des Plots einstellen, um die Klammer sichtbar zu machen
ax.set_xlim(-0.5, 11)

# y-Achse anpassen, um Platz für die Klammer zu schaffen
ax.spines['left'].set_position(('data', 0))
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('black')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('right')
ax.yaxis.set_label_position('right')
ax.set_xticks(interactions)
formatter = FuncFormatter(lambda y, _: f'{y:.0f}%' if y <= 0 else f'+{y:.0f}%' )
ax.yaxis.set_major_formatter(formatter)

ax.set_ylabel('Time advantage\nof voice control'+r' [\%]')
ax.set_xlabel('Number of steps in task [ ]')

set_one_label_upside(ax)

# Plot anzeigen
save_my_figures("voice_control_industrial", fig=fig, bbox_extra_artists=[kl1, kl2])
my_plt.show()