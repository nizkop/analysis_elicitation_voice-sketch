from src.color_codes import global_colors
from src.plt_settings import my_plt, save_my_figures, default_height, figure_width

sketch_and_voice = 147
sketch = 513
voice = 267
gui = 136

total = sketch_and_voice+sketch+gui+voice
assert total == 1063


labels = ['voice+sketch', 'sketch', 'voice', 'GUI']
values = [147, 513, 267, 136]

#
# # Pie Chart erstellen
# fig, ax = my_plt.subplots(figsize=(figure_width, default_height*0.9))
# my_plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140,
#         colors=[global_colors[label] for label in labels],
#            textprops={'fontweight': 'bold'}
#            )
# my_plt.axis('equal')
# my_plt.tight_layout()
# save_my_figures(name="circle", fig=fig)
# my_plt.show()

from src.color_codes import global_colors
from src.plt_settings import my_plt, save_my_figures, default_height, figure_width

colors = [global_colors[label] for label in labels]

fig, ax = my_plt.subplots(figsize=(figure_width * 0.15, default_height*0.81))

bottom = 0
for value, label, color in zip(values, labels, colors):
    percent = value / total * 100
    ax.bar(
        x=0, height=percent, bottom=bottom,
        color=color, width=0.6
    )
    ax.text(
        x=0,
        y=bottom + percent / 2,
        s=fr'{percent:.1f}%',
        va='center', ha='center',
        color='white',
        fontsize=16,
        fontweight='bold'
    )
    bottom += percent

ax.set_ylim(0, 100)
ax.set_yticks([])
ax.set_xlim(-0.3, 0.3)
ax.set_xticks([])
my_plt.tight_layout()
save_my_figures(name="stacked_bar_vertical", fig=fig)
my_plt.show()
