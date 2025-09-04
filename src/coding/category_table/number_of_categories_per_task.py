from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

from src.Tasks.information_about_tasks_in_topic_order import set_topics_as_ticks_to_axis
from src.Tasks.task_topic import topic_order
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.get_category_table_of_selected_tasks import get_category_table_of_selected_tasks
from src.coding.getting_coding_categories import get_color
from src.get_descriptions import names
from src.plt_settings import figure_width, default_height, my_plt, save_my_figures

from collections import Counter


fig, ax = my_plt.subplots(figsize=(figure_width, default_height*0.75))
reference_order = None
for coding_category in CODING_CATEGORIES:
    if coding_category == CODING_CATEGORIES.EMPTYMOD:
        continue
    number_of_categories_per_task = Counter()
    for topic in topic_order:
        df, counts = get_category_table_of_selected_tasks(task_topic=topic, limit_to=coding_category)
        number_of_categories_per_task += Counter(counts)

    if reference_order is None:
        reference_order = list(number_of_categories_per_task.keys())


    y = [number_of_categories_per_task[i] for i in reference_order]
    color, alpha, marker, linestyle = get_color(coding_category)

    ax.plot(reference_order, y, label=coding_category.value, color=color, linestyle=linestyle, marker=marker, alpha=alpha)




ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xticklabels(reference_order, rotation=45, ha='right')
ax.set_xlabel(names["taskid"])
ax.set_ylabel('Number of Categories [ ]')

handles = []
for limit_to in [CODING_CATEGORIES.FULLMOD, CODING_CATEGORIES.OPERATIONMOD, CODING_CATEGORIES.LOCATIONMOD,
                 CODING_CATEGORIES.FULLMODLESS, CODING_CATEGORIES.OPERATIONMODLESS, CODING_CATEGORIES.LOCATIONMODLESS,
                 ]:
    color, alpha, marker, linestyle = get_color(limit_to)
    entry = Line2D([0], [0], color=color, marker=marker, linestyle=linestyle, alpha=alpha, label=limit_to.value)
    handles.append(entry)
legend = ax.legend(title=names["level"] +":",
                    handles= handles,
                    loc='upper left',
                    bbox_to_anchor=(0.4, 1.49),
                    ncol=2)
set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.4)
save_my_figures("number_of_categories_per_task", fig=fig, bbox_extra_artists=[legend])
my_plt.show()