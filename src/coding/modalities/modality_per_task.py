import numpy as np
import matplotlib.patches as mpatches

from src.Tasks.Task import tasks
from src.Tasks.information_about_tasks_in_topic_order import get_tasks_in_topic, set_topics_as_ticks_to_axis
from src.color_codes import global_colors
from src.get_descriptions import names
from src.participants import participants
from src.plt_settings import my_plt, figure_width, default_height, save_my_figures, size_2


def modality_choice_per_task(modalities:list[str]):
    tasks_modalities_counts = {}# im Stil: task_id: percentages

    tasks_along_topics = get_tasks_in_topic()
    for task in tasks_along_topics:
        used_modalities_amounts = { mod: 0 for mod in modalities}
        participant_count = 0

        for p in participants:
            if task.coded(p=p) and not task.missunderstood(p) and not task.skipped(p):
                participant_count += 1
                category_array = task.get_category(p=p)
                category_array = [i.lower() for i in category_array if i is not None]
                for category in category_array:
                    if "gui" in category:
                        used_modalities_amounts["GUI"] += 1
                    if "sketch" in category and not "voice" in category:
                        used_modalities_amounts["sketch"] += 1
                    if "voice" in category and not "sketch" in category:
                        used_modalities_amounts["voice"] += 1
                    if "voice" in category and "sketch" in category:
                        used_modalities_amounts["voice+sketch"] += 1

        if participant_count == 0:
            raise Exception(f"No valid participant data for task {task.id}")

        total_amount = sum(used_modalities_amounts.values())
        percentage_counts = {key: 100*value/total_amount for key, value in used_modalities_amounts.items()}
        tasks_modalities_counts[task.identifier] = percentage_counts

    # Check if any modality was never used in any task
    for task, task_results in tasks_modalities_counts.items():
        for mod, percentage in task_results.items():
           if percentage == 0:
                print(f"! Modality '{mod}' was not used in task {task}")
    return tasks_modalities_counts


def plot_modality_choice_per_task(modalities:list[str]):
    tasks_modalities_counts = modality_choice_per_task(modalities)
    s_SV = ""
    s_GUI = ""
    s_S = ""
    s_V = ""

    fig, ax = my_plt.subplots(figsize=(figure_width, default_height))

    task_tick = 0
    labels = []
    for task, percentages in tasks_modalities_counts.items():
        # print(task,":", percentages)
        labels.append(task)
        unten = 0
        for mod in modalities:
            height = percentages[mod]
            if mod =="voice+sketch":
                s_SV += f"Value for 'voice+sketch', task {task},	 {round(height,1)} ,%\n"
            elif mod == "sketch":
                s_S  += f"Value for 'sketch', task {task},	 {round(height,1)} ,%\n"
            elif mod == "voice":
                s_V  += f"Value for 'voice', task {task},	 {round(height,1)} ,%\n"
            elif mod == "GUI":
                s_GUI  += f"Value for 'GUI', task {task},	 {round(height,1)} ,%\n"
            ax.bar(x=task_tick, height=height, bottom=unten, label=mod, color=global_colors[mod], width=0.9)
            ax.text(task_tick, unten + height / 2, f"{height:.1f}", ha='center', va='center', color='black', fontsize=size_2)
            unten += height
        task_tick += 1

    set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.44)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45)
    ax.set_xlabel(names["taskid"])
    ax.set_ylabel(names["taskNO"])
    ax.set_ylim(0, 100)

    patch_sketch = mpatches.Patch(color=global_colors["sketch"], label='sketch')
    patch_voice = mpatches.Patch(color=global_colors["voice"], label='voice')
    patch_overlap = mpatches.Patch(color=global_colors["voice+sketch"], label='voice+sketch')
    patch_gui = mpatches.Patch(color=global_colors["GUI"], label='GUI')
    legend = ax.legend(loc='upper center',
                       labels=['Sketching', 'Vocalizing', 'Sketch+Voice', "GUI"],
                       handles=[patch_sketch, patch_voice, patch_overlap, patch_gui],
                       bbox_to_anchor=(0.572, 1.2),
                       borderaxespad=0,
                       title=names["modality"]+":",
                       ncol=4)

    save_my_figures("preferred_modality_per_task", fig=fig, bbox_extra_artists=[legend])
    my_plt.show()
    my_plt.close()


    for set in [("GUI", s_GUI), ("sketch", s_S), ("voice", s_V), ("voice+sketch", s_SV)]:
        with open(f'percentages_modality_{set[0]}.csv', 'w') as f:
            f.write(set[1])


if __name__ == "__main__":
    modalities = ["sketch", "voice", "voice+sketch", "GUI"]
    plot_modality_choice_per_task(modalities)
