from src.Tasks.create_topic_axis import create_topic_axis
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height
from src.QuestionnaireOption import QuestionnaireOption
from src.Tasks.Task import tasks
from src.TaskJsonKind import TaskJsonKind
from src.participants import participants
from src.color_codes import global_colors
from src.languages.translation import translation
from src.get_descriptions import names

from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches




def generate_difficulty_data(tasks, participants):
    """
    Gibt eine Liste zurück mit (task_identifier, options_dict),
    wobei options_dict eine Dikt mit {option_label: count} ist.
    """
    all_data = []
    for task in tasks:
        if task.identifier.lower() in ["c", "g"]:
            continue

        perceived_difficulty = {}
        for p in participants:
            data = task.get_dictionary(p, infokind=TaskJsonKind.QUESTION)
            if data is not None and not (task.skipped(p) or task.missunderstood(p)):
                key = translation(data[task.difficulty_question])
                try:
                    perceived_difficulty[key].append(p.id)
                except KeyError:
                    perceived_difficulty[key] = [p.id]
            elif task.skipped(p) or task.missunderstood(p):
                try:
                    perceived_difficulty["skipped/missunderstood"].append(p.id)
                except KeyError:
                    perceived_difficulty["skipped/missunderstood"] = [p.id]
            else:
                if p.id == "000":
                    continue
                raise Exception("what happened?", p.id, task.identifier)

        options = {option.value: 0 for option in QuestionnaireOption}
        for k in perceived_difficulty.keys():
            options[k] = len(perceived_difficulty[k])

        all_data.append((task.identifier, task.get_group(), options))
    return all_data


def plot_stacked_bar(data, x_positions=None, bar_width=2, group_spacing=0.5):
    fig, ax = my_plt.subplots(figsize=(figure_width, default_height))

    x_ticks = []
    x_labels = []
    used_labels = {}

    for i, (task_identifier, group, options) in enumerate(data):
        x = x_positions[i] if x_positions else i * (bar_width + group_spacing)
        bottom = 0

        for label, count in options.items():
            used_labels[label] = global_colors[label]
            ax.bar(x, count, width=bar_width, color=global_colors[label], bottom=bottom, alpha=1)
            bottom += count

        x_ticks.append(x)
        x_labels.append(str(task_identifier))

    # Rest vom Code für Achsen, Legende etc.
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.set_xlabel(names["taskid"])
    ax.set_ylabel(names["participantNO"])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    patches = [mpatches.Patch(color=color, label=label) for label, color in used_labels.items()]
    legend = ax.legend(handles=patches, title=names["option"]+":", bbox_to_anchor=(0.215, 1.34), loc='upper left', ncol = 3)

    return ax, fig, legend


def add_distance_between_groups(data, bar_width=2.0, task_spacing=0.5, group_spacing=2.0):
    """
    Berechnet x-Positionen für Tasks mit größeren Abständen zwischen Gruppen.

    :param data: Liste von (task_id, group_id, options_dict), bereits sortiert nach group_id
    :param bar_width: Breite der Balken
    :param task_spacing: Abstand zwischen Tasks innerhalb der gleichen Gruppe
    :param group_spacing: Abstand vor einer neuen Gruppe (größer als task_spacing)

    :return: Liste von x-Positionen (float), passend zu data
    """
    x_positions = []
    current_x = 0
    previous_group = None

    for _, group_id, _ in data:
        if previous_group is None:
            # erster Task, kein Abstand
            pass
        elif group_id != previous_group:
            # neue Gruppe: größeren Abstand vor Balken
            current_x += group_spacing
        else:
            # gleiche Gruppe: kleinerer Abstand
            current_x += task_spacing

        x_positions.append(current_x)
        current_x += bar_width
        previous_group = group_id

    return x_positions





def add_group_secondary_xaxis(ax, data, fig, x_positions:list, bar_width=2):
    """
    Fügt dem Plot eine zweite x-Achse oben hinzu, die die Gruppenzugehörigkeit anzeigt.
    Zusätzlich werden farbige Balken (hinterlegt) über den Bereich jeder Gruppe gelegt.

    :param ax: matplotlib Axes-Objekt des bestehenden Plots
    :param data: Liste von (task_id, group_id, options_dict), sortiert nach group_id
    :param x_positions: Liste von x-Positionen für Tasks (gleiche Länge wie data)
    :param bar_width: Breite der Balken (float)
    :param group_colors: dict {group_id: Farbe} für Hintergrundfarben der Gruppen. Wenn None, werden Blautöne verwendet.
    """
    # topics_with_x_values = get_xvalues_of_topic()
    # create_topic_axis(fig=fig, ax_main=ax, topics_with_x_values=topics_with_x_values, extrawidth=extrawidth)

    group_x_values = {}
    for i in range(len(x_positions)):
        taskid = data[i][0]
        group = data[i][1]
        x = x_positions[i]
        groupname = names[f"group{group}"]
        if groupname not in group_x_values:
            group_x_values[groupname] = []
        group_x_values[groupname].append(x)

    ax_topic = create_topic_axis(fig=fig, ax_main=ax, topics_with_x_values=group_x_values, extrawidth=bar_width//2)
    ax_topic.set_xlabel(names["group"])
    return
    # # Erstelle secondary x-axis oben
    # secax = ax.secondary_xaxis('top')
    # secax.set_xlabel(names["group"])
    # secax.set_xlim(ax.get_xlim())
    #
    # # Balken/Flächen für Gruppen auf dem primären Axes (unten)
    # for group, start_idx, end_idx in group_boundaries:
    #     x_start = x_positions[start_idx] - bar_width/2
    #     x_end = x_positions[end_idx] + bar_width/2
    #     color = group_colors.get(group, 'lightblue')
    #
    #     # Rechteck als Hintergrund (über primärer Achse)
    #     ax.axvspan(x_start, x_end, ymin=0, ymax=1, facecolor=color, alpha=0.15, zorder=-1)
    #
    # # Positionen für Gruppenlabels auf secondary axis
    # group_centers = []
    # group_labels = []
    # for group, start_idx, end_idx in group_boundaries:
    #     x_center = (x_positions[start_idx] + x_positions[end_idx]) / 2
    #     group_centers.append(x_center)
    #     group_labels.append(names[f"group{group}"])
    #
    # secax.set_xticks(group_centers)
    # secax.set_xticklabels(group_labels, fontsize=12, rotation=0)



def overview_difficulty_tasks():
    data = generate_difficulty_data(tasks, participants)
    sorted_data = sorted(
        data,
        key=lambda x: (x[1], -x[2].get("very easy", 0))  # Sortiere nach Group aufsteigend, dann nach "very easy" absteigend
    )
    summe = 0
    for i in sorted_data:
        print(i[0], "very easy = ", i[2]["very easy"] / sum(i[2].values()))
        summe += sum(i[2].values())
    print(summe)


    xaxispositions = add_distance_between_groups(sorted_data)# ! nach sorting
    ax, fig, legend = plot_stacked_bar(sorted_data, bar_width=2, group_spacing=0.5, x_positions=xaxispositions)

    # add_group_secondary_xaxis(ax, sorted_data, xaxispositions, bar_width=2)
    add_group_secondary_xaxis(fig=fig, ax=ax, data=sorted_data, bar_width=2, x_positions=xaxispositions)

    savefile="difficulty_of_tasks_stacked"
    if savefile:
        save_my_figures(savefile, fig=fig, bbox_extra_artists=[legend])
    my_plt.show()
    my_plt.close()



if __name__ == '__main__':
    overview_difficulty_tasks()