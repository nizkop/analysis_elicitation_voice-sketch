import pandas as pd
from matplotlib.patches import Patch
import numpy as np

from src.plt_settings import my_plt, save_my_figures, default_height, figure_width
from src.Tasks.Task import tasks
from src.color_codes import global_colors
from src.participants import participants
from src.get_descriptions import names



def plot_box_task(collected_data: list[dict], x_name: str, xlabel:str, break_axis:bool):
    # Sortierung z.B. nach Median der x_werte und Gruppierung
    collected_data.sort(key=lambda x: (
        {"A": 1, "B": 2, "C": 3, "P": 0}.get(x["group"], -1),  # Sortiere nach Gruppenreihenfolge, unbekannte Gruppen kommen ans Ende
        np.median(x["times"]) if x["times"] else float('inf')  # Innerhalb Gruppe nach Median sortieren
        #str(x["id"])
    ))
    labels = [c["id"] for c in collected_data]
    groups = [c["group"] for c in collected_data]
    colors = [c["color"] for c in collected_data]
    x_list = [c[x_name] for c in collected_data]

    if break_axis:
        fig, (ax2, ax) = my_plt.subplots(2, 1, sharex=False,figsize=(figure_width, default_height),
                                         gridspec_kw={'height_ratios': [1, 10], "hspace": 0.05})

        # plot the same data on both Axes
        box = ax2.boxplot(x_list, patch_artist=True, tick_labels=labels, showfliers=True)
        for flier, color in zip(box['fliers'], colors):
            flier.set(marker='o', markeredgecolor=color, markerfacecolor='white', markersize=6)
        box = ax.boxplot(x_list, patch_artist=True, tick_labels=labels, showfliers=True)

        max_outlier = max([max(i) for i in x_list])
        ax2.set_ylim(max_outlier-max_outlier/100,max_outlier+max_outlier/100)  # outliers only
        hochster_wishker = max([np.percentile(y_values, 75) for y_values in x_list])
        if x_name == "times":
            factor = 1.3#2.4
        elif x_name == "switch_amount":
            factor = 1.4#2.4
        ax.set_ylim(0, hochster_wishker+hochster_wishker/factor)  # most of the data

        ax2.set_yticks([max_outlier])
        ax2.set_yticklabels([f"{max_outlier:.0f}"])

        # hide the spines between ax and ax2
        ax2.spines.bottom.set_visible(False)
        ax.spines.top.set_visible(False)
        ax2.xaxis.tick_top()
        # ax2.tick_params(labeltop=False)  # no tick labels at the top
        ax.xaxis.tick_bottom()

        d = .5  # Schrägheitsmaß der Unterbrechungslinie
        kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                      linestyle="none", color='k', mec='k', mew=1, clip_on=False)
        ax2.plot([0, 1], [0, 0], transform=ax2.transAxes, **kwargs)
        ax.plot([0, 1], [1, 1], transform=ax.transAxes, **kwargs)
    else:
        fig, ax = my_plt.subplots(figsize=(figure_width, default_height))
        ax2 = None
        box = ax.boxplot(x_list, patch_artist=True, labels=labels, showfliers=True)
    # Farben zuweisen
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    for flier, color in zip(box['fliers'], colors):
        flier.set(marker='o', markeredgecolor=color, markerfacecolor='white', markersize=6)
    ax.set_xlabel(names["taskid"])
    ax.set_ylabel(xlabel)
    my_plt.xticks(rotation=45)
    # Legende basierend auf Gruppen:
    legend_elements = [Patch(facecolor=color,
                                 label=names[group])
                           for group, color in global_colors.items()
                           if group is not None and "group" in group and group != "groupP"
                          ]
    legend = fig.legend(handles=legend_elements, title=names["group"] + ":",
                            loc='upper left',
                            bbox_to_anchor=(0.5685, 1.13),
                            ncol=3)
    save_my_figures(f"boxplot_watching_{x_name}_tasks", fig=fig, bbox_extra_artists=[legend])
    my_plt.show()
    # my_plt.close()
    return fig, ax, ax2, legend


def get_box_task(x_name, break_axis:bool=True):
    csv_zeilen = []
    csv_zeilen_switch = []
    collected_data = []
    for task_idx, task in enumerate(tasks):
        if task.identifier.lower() not in ["c", "g"]:
            times = task.median_watching_time(participants)
            for t in times:
                csv_zeilen.append( {"TaskID": f"{task.identifier}", "Time": f"{t}"} )
            switches = None
            if x_name == "times":
                xlabel = "Watching Time [s]"
            elif x_name == "switch_amount":
                switches = task.get_switch_median(participants)
                for s in switches:
                    csv_zeilen_switch.append( {"TaskID": f"{task.identifier}", "Switches": f"{s}"} )
                xlabel = "Switch Number [ ]"
            else:
                raise Exception("unknown x_name", x_name)
            collection = {
                "times": times,
                "switch_amount": switches,
                "id": task.identifier,
                "group": task.get_group(),
                "color": global_colors.get("group"+task.get_group() if task.get_group() else None)
            }
            collected_data.append(collection)
    df_times = pd.DataFrame(csv_zeilen)
    df_times.to_csv("boxplot_times.csv", sep=",", index=False)

    df_switches = pd.DataFrame(csv_zeilen_switch)
    df_switches.to_csv("boxplot_switches.csv", sep=",", index=False)
    fig, ax, ax2, legend = plot_box_task(collected_data, x_name, xlabel=xlabel, break_axis=break_axis)

    if x_name == "times":
        return df_times, fig, ax, ax2, legend
    else:
        return df_switches, fig, ax, ax2, legend



if __name__ == "__main__":
    # get_box_task("times", True)
    get_box_task("switch_amount", True)