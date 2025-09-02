from src.Tasks.information_about_tasks_in_topic_order import set_topics_as_ticks_to_axis
from src.Tasks.task_topic import topic_order
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.get_category_table_of_selected_tasks import get_category_table_of_selected_tasks
from src.coding.getting_coding_categories import get_color
from src.get_descriptions import names
from src.plt_settings import figure_width, default_height, my_plt, save_my_figures

from collections import Counter


fig, ax = my_plt.subplots(figsize=(figure_width, default_height))
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

ax.set_xticklabels(reference_order, rotation=45, ha='right')
ax.set_xlabel(names["taskid"])
ax.set_ylabel('Number of Categories [ ]')
legend = ax.legend(title=names["level"]+":", loc='upper right',
                        bbox_to_anchor=(1.01,1.36),
                        ncol=2)
set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.4)
save_my_figures("number_of_categories_per_task", fig=fig, bbox_extra_artists=[legend])

my_plt.show()