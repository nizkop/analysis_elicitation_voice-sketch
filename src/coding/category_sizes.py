import numpy as np

from src.Tasks.information_about_tasks_in_topic_order import get_tasks_in_topic, set_topics_as_ticks_to_axis
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.get_categories_for_tasks import get_categories_for_tasks
from src.color_codes import global_colors
from src.get_descriptions import names
from src.plt_settings import figure_width, default_height, my_plt, save_my_figures

tasks = get_tasks_in_topic()
coding_data, information_about_agreement_rate, task_names = get_categories_for_tasks(tasks, limit_to=CODING_CATEGORIES.FULLMOD)
all_category_sizes = set()
for categories in information_about_agreement_rate.values():
    for cat in categories:
        all_category_sizes.add(cat.count("-") + 1)
all_category_sizes = sorted(all_category_sizes)


task_ids = list(information_about_agreement_rate.keys())

data_matrix = []
for size in all_category_sizes:
    counts = []
    for task in task_ids:
        category_sizes = {}
        for cat in information_about_agreement_rate[task]:
            n = cat.count("-") +1
            category_sizes[n] = category_sizes.get(n, 0) +1
        counts.append(category_sizes.get(size, 0))
    data_matrix.append(counts)



fig, ax = my_plt.subplots(figsize=(figure_width,default_height))
bottom = np.zeros(len(task_ids))
for idx, size in enumerate(all_category_sizes):
    ax.bar(task_ids, data_matrix[idx], bottom=bottom,
           color=global_colors[f"category_size_{size}"], label=f'{size} Codes')
    bottom += np.array(data_matrix[idx])

ax.set_xlabel(names['taskid'])
ax.set_ylabel('Size of Categories [ ]')
legend = ax.legend(title='Category Size:', loc='upper right',
                        bbox_to_anchor=(1.01,1.3),
                        ncol=2)
my_plt.xticks(rotation=45)
set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.4)
save_my_figures("size_of_categories_per_task", fig=fig, bbox_extra_artists=[legend])
my_plt.show()