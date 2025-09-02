import numpy as np
import pandas as pd

from src.plt_settings import my_plt, figure_width, default_height
from src.Tasks.Task import tasks, Task
from src.TaskJsonKind import TaskJsonKind
from datetime import datetime
from matplotlib.patches import Patch

from src.color_codes import global_colors
from src.get_descriptions import names
from src.participants import participants
from src.plt_settings import save_my_figures


def time_needed_modalities_get_data():
    total_time_voice = []
    total_time_sketch = []
    # diagram
    x = []
    y_voice = []
    y_sketch = []
    y_voice_std = []
    y_sketch_std = []
    for task in tasks:
        time_voice = []
        time_sketch = []
        for p in participants:
            # print("p", p.id, "task", task.identifier)
            category_array = task.get_category(p=p)
            if category_array is not None:
                category_array = [i.lower() for i in category_array if i is not None]
            if category_array is not None and len(category_array) > 0:
                if "gui" in "".join(category_array).lower():
                    continue
                if "skipped" in "".join(category_array).lower():
                    continue
                if "sketch" in "".join(category_array) and "voice" in "".join(category_array):
                    # mixed not usable to determine length of pure voice & pure sketch part
                    continue
                info_dict = task.get_dictionary(p=p, infokind=TaskJsonKind.INFO)
                if info_dict is None:
                    continue
                info = info_dict["taskData"]
                if info is None:
                    continue
                if "voice" in "".join(category_array) and len(info["startTimeVoice"]) > 0 and len(info["endTimeVoice"]) > 0:
                    try:
                        start_time = datetime.strptime(info["startTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        end_time = datetime.strptime(info["endTimeVoice"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        if (end_time - start_time).total_seconds() <= 0:
                            print("stange timing voice p", p.id, "task", task.identifier)
                        total_time_voice.append( abs( start_time - end_time ).total_seconds() )
                        time_voice.append( abs( start_time - end_time ).total_seconds() )
                    except ValueError as e:
                        raise Exception(f"participant {p.id}, task {task.identifier}: {e}")
                if "sketch" in "".join(category_array) and len(info["startTimeDrawing"]) > 0 and len(info["endTimeDrawing"]) > 0:
                    start_time = datetime.strptime(info["startTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    end_time = datetime.strptime(info["endTimeDrawing"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    if (end_time - start_time).total_seconds() <= 0:
                        print("stange timing sketch p", p.id, "task", task.identifier)
                    total_time_sketch.append(abs(start_time - end_time).total_seconds() )
                    time_sketch.append( abs( start_time - end_time ).total_seconds() )

        if len(time_voice) > 0 and len(time_sketch) > 0:
            x.append(task.identifier)
            y_voice.append(time_voice)
            y_sketch.append(time_sketch)
    return x, y_voice, y_sketch

def time_needed_modalities_sort_data(x, y_voice, y_sketch):
    #Sortierung innerhalb task-Gruppen, dann nach median von y
    task_groups = [Task(x_i).get_group() for x_i in x]
    medians_voice = np.array([np.median(times) if len(times) > 0 else np.inf for times in y_voice])
    sorted_indices = np.lexsort((medians_voice, task_groups))# erst Sortieren nach group, innerhalb group sortieren nach medians

    x_sorted = np.array(x)[sorted_indices]
    y_voice_sorted = np.array(y_voice, dtype=object)[sorted_indices]
    y_sketch_sorted = np.array(y_sketch, dtype=object)[sorted_indices]

    return x_sorted, y_voice_sorted, y_sketch_sorted

def time_needed_modalities_plot(x_sorted, y_voice_sorted, y_sketch_sorted, break_axis:bool = False):
    # Box-plot:
    collected_data = []
    offset = 0.175
    positions_voice = np.arange(len(x_sorted)) - offset
    positions_sketch = np.arange(len(x_sorted)) + offset
    if not break_axis:
        fig, ax = my_plt.subplots(figsize=(figure_width, default_height))
    else:
        task_group = [Task(i).get_group() for i in x_sorted]
        for i in range(len(y_sketch_sorted)):
            for j in range(len(y_sketch_sorted[i])):
                collection = {
                    "id": x_sorted[i],
                    "group": Task(x_sorted[i]).get_group(),
                    "modality": "sketch",
                    "time": y_sketch_sorted[i][j],
                    "topic": Task(x_sorted[i]).topic.name,
                }
                collected_data.append(collection)
        for i in range(len(y_voice_sorted)):
            for j in range(len(y_voice_sorted[i])):
                collection = {
                    "id": x_sorted[i],
                    "group": Task(x_sorted[i]).get_group(),
                    "modality": "voice",
                    "time": y_voice_sorted[i][j],
                    "topic": Task(x_sorted[i]).topic.name,
                }
                collected_data.append(collection)

        fig, (ax2, ax) = my_plt.subplots(2, 1, sharex=False,figsize=(figure_width, 6),
                                         gridspec_kw={'height_ratios': [1, 10], "hspace": 0.05})
        box_voice = ax2.boxplot(y_voice_sorted, positions=positions_voice, widths=0.25, patch_artist=True, showfliers=True)
        box_sketch = ax2.boxplot(y_sketch_sorted, positions=positions_sketch, widths=0.25, patch_artist=True, showfliers=True)
        for flier in box_voice['fliers']:
            flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['voice'], alpha=1,
                      markersize=6)
        for flier in box_sketch['fliers']:
            flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['sketch'], alpha=1,
                      markersize=6)

        max_outlier = max([max(i) for i in y_voice_sorted+y_sketch_sorted])
        q1 = max([np.percentile(y, 25) for y in y_voice_sorted+y_sketch_sorted])
        q3 = max([np.percentile(y, 75) for y in y_voice_sorted+y_sketch_sorted])
        highest_wisker = q3 + 1.2 * (q3 - q1)
        ax2.set_ylim(max_outlier - max_outlier / 100, max_outlier + max_outlier / 100)  # outliers only
        hoechster_boxrand = max([np.percentile(y_values, 75) for y_values in y_voice_sorted+y_sketch_sorted])
        ax.set_ylim(0, highest_wisker) #hoechster_boxrand + hoechster_boxrand / 5)  # most of the data

        ax2.set_yticks([max_outlier])
        ax2.set_yticklabels([f"{max_outlier:.0f}"])

        # hide the spines between ax and ax2
        ax2.spines.bottom.set_visible(False)
        ax.spines.top.set_visible(False)
        ax2.xaxis.tick_top()
        # ax2.tick_params(labeltop=False)  # don't put tick labels at the top
        ax.xaxis.tick_bottom()

        d = .5  # Schrägheitsmaß der Unterbrechungslinie
        kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                      linestyle="none", color='k', mec='k', mew=1, clip_on=False)
        ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, **kwargs)
        ax.plot([0, 1], [1, 1], transform=ax.transAxes, **kwargs)

        unique_groups = []
        positions = []
        for group in sorted(set(task_group), key=task_group.index):  # Reihenfolge wie im Original
            indices = [i for i, g in enumerate(task_group) if g == group]
            mean_pos = np.mean(indices)
            unique_groups.append(group)
            positions.append(mean_pos)

        ax2.set_xticks(positions)
        ax2.set_xticklabels([names[f"group{i}"] for i in unique_groups], rotation=0)
        ax2.tick_params(axis='x', width=len(x_sorted) *28.5/ len(unique_groups))
        ax2.xaxis.set_label_position('top')
        ax2.set_xlabel(names["group"])

    box_voice = ax.boxplot(y_voice_sorted, positions=positions_voice, widths=0.25, patch_artist=True, showfliers=True)
    box_sketch = ax.boxplot(y_sketch_sorted, positions=positions_sketch, widths=0.25, patch_artist=True, showfliers=True)
    for patch in box_voice['boxes']:
        patch.set_facecolor(global_colors['voice'])
    for patch in box_sketch['boxes']:
        patch.set_facecolor(global_colors['sketch'])
    for flier in box_voice['fliers']:
        flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['voice'], alpha=1, markersize=6)
    for flier in box_sketch['fliers']:
        flier.set(marker='o', markerfacecolor='white', markeredgecolor=global_colors['sketch'], alpha=1, markersize=6)


    ax.set_xticks(np.arange(len(x_sorted)))
    ax.set_xticklabels(x_sorted, rotation=45)
    ax.set_ylabel(names["time"])

    my_plt.ylim(bottom=0, top=None)
    ax.tick_params(axis='x', width=offset*109)
    ax.set_xlabel(names["taskid"])
    my_plt.ylabel("Time Spend\nCreating a Command [s]")
    legend_elements = [
        Patch(facecolor=global_colors['voice'], label='Voice'),
        Patch(facecolor=global_colors['sketch'], label='Sketch')
    ]
    legend = my_plt.legend(handles=legend_elements, title=names["modality"] + ":",
                  loc='upper left', bbox_to_anchor=(0.65, 1.41), ncol=2)
    # my_plt.tight_layout()
    save_my_figures("time_needed_modalities", fig=fig, bbox_extra_artists=[legend])
    my_plt.show()
    # print("voice", np.median(total_time_voice))
    # print("sketch", np.median(total_time_sketch))

    data_table = pd.DataFrame(collected_data)
    data_table.to_csv("boxplot_time_needed.csv", sep=",", index=False)
    return data_table, fig, ax, ax2


def time_needed_modalities():
    x, y_voice, y_sketch = time_needed_modalities_get_data()
    x_sorted, y_voice_sorted, y_sketch_sorted = time_needed_modalities_sort_data(x, y_voice, y_sketch)
    return time_needed_modalities_plot(x_sorted, y_voice_sorted, y_sketch_sorted, True)






if __name__ == "__main__":
    data_table, fig, ax, ax2 = time_needed_modalities()