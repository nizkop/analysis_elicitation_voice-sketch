from matplotlib import patches
from matplotlib.lines import Line2D

from src.Tasks.information_about_tasks_in_topic_order import set_topics_as_ticks_to_axis
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.table_choice.get_color_style import get_color_style
from src.get_descriptions import names
from src.plt_settings import figure_width, default_height, my_plt, save_my_figures, footnotesize, size_2
from src.Tasks.task_topic import topic_order


def plot_operation_relative_values_with_lines(filename, df_percent, amount_of_tasks_per_topic:list[int],
                                              coding_category:CODING_CATEGORIES):
    if coding_category == CODING_CATEGORIES.OPERATIONMODLESS:
        y_columns = [col for col in df_percent.columns if col.startswith('operation')]
    elif coding_category == CODING_CATEGORIES.LOCATIONMODLESS:
        y_columns = [col for col in df_percent.columns if col.startswith('location')]
    (fig, ax) = my_plt.subplots(figsize=(figure_width, default_height*0.75))

    y_columns.sort(key=len, reverse=True)
    for col in y_columns:
        marker, color, title = get_color_style(col)
        ax.plot(df_percent['Task'], df_percent[col], marker=marker, color=color, label=title, alpha=1)

    my_plt.xlabel(names["taskid"])
    my_plt.ylabel(r'Use of Category for given Task [\%]')
    x = range(len(df_percent))
    x_labels = [str(s).replace("task ", "") for s in df_percent['Task']]
    ax.set_xticks(ticks=x, labels=x_labels, rotation=45)

    change_positions = [sum(amount_of_tasks_per_topic[:i])-0.5 for i in range(len(amount_of_tasks_per_topic))]
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax + 5)
    for i in range(len(change_positions)):
        pos = change_positions[i]
        if i != 0:
            ax.axvline(x=pos, color='black', linestyle='dotted', alpha=1)
    set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.35)

    legend = get_legend(ax, coding_category)
    save_my_figures(filename, bbox_extra_artists=[legend])
    fig.show()
    return


def get_legend(ax, coding_category:CODING_CATEGORIES):
    if coding_category == CODING_CATEGORIES.OPERATIONMODLESS:
        handles = []
        for i in ["operation:words", "operation:symbol", "operation:symbol - operation:words"]:
            marker, color, label = get_color_style(i)
            line = Line2D([0], [0], color=color, marker=marker, linestyle='-', label=label)
            handles.append(line)
        return ax.legend(handles=handles, title=f"Coded Category in level {CODING_CATEGORIES.OPERATIONMODLESS.value}:",
                           loc='upper left', title_fontsize=size_2,
                           bbox_to_anchor=(-0.0265, 1.38),
                           ncol=2)
    if coding_category == CODING_CATEGORIES.LOCATIONMODLESS:
        entries_simple = ["location:entry", "location:pointing", "location:address"]
        x_simple = -0.09
        y_long = 1.458
        y_simple = 1.534
        entries_long = ["location:entry - location:address", "location:address - location:pointing",
                      "location:entry - location:pointing",
                      "location:entry - location:address - location:pointing"]
        dummy_entries = ["location:entry", "location:entry", "location:entry"]*5
        dummy_handles = []
        for i in dummy_entries:
            marker, color, label = get_color_style(i)
            line = Line2D([0], [0], color=color, marker=marker, linestyle='-',
                          label=label+r"°.°", alpha=0)
            dummy_handles.append(line)
        legend_dummy = ax.legend(handles=dummy_handles,
                           title=f"Coded Category in level {CODING_CATEGORIES.LOCATIONMODLESS.value}:",
                           loc='upper left', title_fontsize=size_2,# textcolor="white",
                           bbox_to_anchor=(x_simple, y_simple+0.085), frameon=True,
                           ncol=3)
        for text in legend_dummy.get_texts():
            text.set_color((1, 1, 1, 0))  # Weiß, mit alpha = 0
        ax.add_artist(legend_dummy)
        handles = []
        for i in entries_simple:
            marker, color, label = get_color_style(i)
            line = Line2D([0], [0], color=color, marker=marker, linestyle='-', label=label)
            handles.append(line)
        legend=ax.legend(handles=handles,
                  # title=f"Coded Category in level {CODING_CATEGORIES.LOCATIONMODLESS.value}:",
                  loc='upper left', title_fontsize=size_2,
                  bbox_to_anchor=(x_simple, y_simple),frameon=False,
                  ncol=3)
        ax.add_artist(legend)
        handles = []
        for i in entries_long:
            marker, color, label = get_color_style(i)
            line = Line2D([0], [0], color=color, marker=marker, linestyle='-', label=label)
            handles.append(line)
        legend2 = ax.legend(handles=handles,
                         #title=f"Coded Category in level {CODING_CATEGORIES.LOCATIONMODLESS.value}:",
                         loc='upper left',title_fontsize=size_2,
                         bbox_to_anchor=(x_simple, y_long),frameon=False,
                         ncol=1)
        return legend_dummy