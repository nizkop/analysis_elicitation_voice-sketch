from matplotlib.lines import Line2D

from src.Tasks.Task import Task
from src.Tasks.information_about_tasks_in_topic_order import set_topics_as_ticks_to_axis, get_tasks_in_topic
from src.Tasks.task_topic import topic_order, topic_order_dict
from src.plt_settings import size_2
from src.get_descriptions import names
from src.plt_settings import my_plt, save_my_figures, figure_width, default_height
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.bootstrap import bootstrap_valbjoern
from src.coding.get_categories_for_tasks import get_categories_for_tasks
from src.color_codes import global_colors


def get_coding_bar_chart(coding_data, task_names, limit_to:CODING_CATEGORIES):
    coding_data.sort(key=lambda d: (d["group"], -d["agreement_rate"]))
    heights = [a["agreement_rate"] for a in coding_data]
    fig, ax = my_plt.subplots(figsize=(figure_width, default_height))
    ax.bar(range(len(coding_data)), heights,
               color=[global_colors["group" + a["group"]] for a in coding_data])
    for i, h in enumerate(heights):
        my_plt.text(i, 0.1, f"{h:.2f}", ha='center', va='center', color='black',
                    fontsize=size_2, rotation=90)

    ax.set_xticks(range(len(coding_data)), [f"{i}" for i in task_names],
                  rotation=45, ha='right', rotation_mode='anchor')

    ax.set_ylim(0, 1)
    ax.set_xlabel(names["taskid"])
    ax.set_ylabel(names["agreement"])
    legend=ax.legend()
    save_my_figures(name=f"agreement_ruffly_{limit_to.name}".replace(" ",""),fig=fig, bbox_extra_artists=[legend])
    fig.show()
    my_plt.close()



def get_coding_dot_chart(coding_data, limit_to:CODING_CATEGORIES, fig=None, ax=None, reference_order=None):
    if fig is None or ax is None:
        fig, ax = my_plt.subplots(figsize=(figure_width, default_height*1))

        hspan_low = ax.axhspan(0.0, 0.1, facecolor=global_colors["low"], alpha=1, label='low')  # < 0.1
        hspan_med = ax.axhspan(0.1, 0.3, facecolor=global_colors["medium"], alpha=1, label='medium')  # 0.1–0.3
        hspan_high = ax.axhspan(0.3, 0.5, facecolor=global_colors["high"], alpha=1, label='high')  # 0.3–0.5
        hspan_veryhigh =ax.axhspan(0.5, 1.0, facecolor=global_colors["veryhigh"], alpha=1, label='very high')  # > 0.5
        legend1 = ax.legend(handles=[hspan_veryhigh, hspan_high, hspan_med, hspan_low],
                            title="Agreement Level:",
                            loc='upper left',
                            bbox_to_anchor=(-0.01, 1.36),
                            ncol = 2)
        ax.add_artist(legend1)
        coding_data.sort(key=lambda d: (topic_order_dict[Task(d["task_name"]).topic], -d["agreement_rate"]))
        reference_order = [a["task_name"] for a in coding_data]
        print("Es wird sortiert nach ", limit_to.value, "innerhalb task topic")
    else:
        #Sortieren nach reference_order:
        coding_data.sort(key=lambda d: reference_order.index(d["task_name"]))
        legend1 = None
    heights = [a["agreement_rate"] for a in coding_data]


    color, alpha, marker, linestyle = get_color(limit_to)
    ax.plot([a["task_name"] for a in coding_data], heights, marker = marker, linestyle=linestyle, color=color,
            markeredgewidth=2,linewidth=2, alpha=alpha, label=limit_to.value)
    legend_entry = Line2D([0], [0], color=color, marker=marker, linestyle=linestyle, label=limit_to.value)
    # legend2 = update_legend(ax, legend2, new_labels=[limit_to.value])
    ax.set_ylim(0, 1)
    ax.set_xlabel(names["taskid"])
    ax.set_ylabel(names["agreement"])
    ax.tick_params(axis='x', rotation=45)
    return fig, ax, legend1, reference_order, legend_entry


def get_color(limit_to:CODING_CATEGORIES):
    marker = "x"
    if limit_to == CODING_CATEGORIES.FULLMODLESS:
        color = global_colors[CODING_CATEGORIES.FULLMOD.name]
        alpha=0.5
        linestyle = "--"
    elif limit_to == CODING_CATEGORIES.OPERATIONMODLESS:
        color = global_colors[CODING_CATEGORIES.OPERATIONMOD.name]
        alpha = 0.5
        linestyle = "--"
    elif limit_to == CODING_CATEGORIES.LOCATIONMODLESS:
        color = global_colors[CODING_CATEGORIES.LOCATIONMOD.name]
        alpha = 0.5
        linestyle = "--"
    elif limit_to == CODING_CATEGORIES.EMPTYMOD:
        linestyle = "dotted"
        marker = "o"
        alpha = 1
        color = global_colors[limit_to.name]
    else:
        color = global_colors[limit_to.name]
        alpha = 1
        linestyle = "-"

    return color, alpha, marker, linestyle



def get_coding_categories(limit_to:CODING_CATEGORIES, fig=None, ax=None, reference_order=None):
    tasks = get_tasks_in_topic()
    coding_data, information_about_agreement_rate, task_names = get_categories_for_tasks(tasks, limit_to=limit_to)

    # Background for each agreement level
    my_plt.axhspan(0.0, 0.1, facecolor=global_colors["low"], alpha=1, label='low')#< 0.1
    my_plt.axhspan(0.1, 0.3, facecolor=global_colors["medium"], alpha=1, label='medium')#0.1–0.3
    my_plt.axhspan(0.3, 0.5, facecolor=global_colors["high"], alpha=1, label='high')#0.3–0.5
    my_plt.axhspan(0.5, 1.0, facecolor=global_colors["veryhigh"], alpha=1, label='very high')#> 0.5

    get_coding_bar_chart(coding_data, task_names, limit_to=limit_to)
    fig, ax, legend1, reference_order, legend_entry = get_coding_dot_chart(coding_data=coding_data, limit_to=limit_to, fig=fig,
                                                                  ax=ax, reference_order=reference_order)

    bootstrap_valbjoern([a["agreement_rate"] for a in coding_data], description=limit_to.name)
    return fig, ax, legend1, reference_order, legend_entry


def run_get_coding_categories():
    # fig, ax, legend1, reference_order, legend_entry7 = get_coding_categories(limit_to=CODING_CATEGORIES.EMPTYMOD, fig=None, ax=None, reference_order=None)

    fig, ax, legend_FULLMOD, reference_order, legend_entry_FULLMOD = get_coding_categories(limit_to=CODING_CATEGORIES.FULLMOD, fig=None, ax=None, reference_order=None)

    fig, ax, xx, reference_order, legend_entry_OPERATIONMOD = get_coding_categories(limit_to=CODING_CATEGORIES.OPERATIONMOD, fig=fig,
                                                                        ax=ax, reference_order=reference_order)
    fig, ax, xx, reference_order, legend_entry_FULLMODLESS = get_coding_categories(limit_to=CODING_CATEGORIES.FULLMODLESS, fig=fig, ax=ax, reference_order=reference_order)
    fig, ax, xx, reference_order, legend_entryOPERATIONMODLESS = get_coding_categories(limit_to=CODING_CATEGORIES.OPERATIONMODLESS, fig=fig, ax=ax, reference_order=reference_order)
    fig, ax, xx, reference_order, legend_entry_LOCATIONMOD = get_coding_categories(limit_to=CODING_CATEGORIES.LOCATIONMOD, fig=fig,
                                                                        ax=ax, reference_order=reference_order)
    fig, ax, xx, reference_order, legend_entry_LOCATIONMODLESS = get_coding_categories(limit_to=CODING_CATEGORIES.LOCATIONMODLESS, fig=fig, ax=ax, reference_order=reference_order)




    legend2 = ax.legend(title=names["level"] +":",
                        handles = [legend_entry_FULLMOD, legend_entry_OPERATIONMOD, legend_entry_LOCATIONMOD,
                                   legend_entry_FULLMODLESS, legend_entryOPERATIONMODLESS, legend_entry_LOCATIONMODLESS,
                                   ],
                        loc='upper left',
                        bbox_to_anchor=(0.4, 1.36),
                        ncol=2)
    ax.add_artist(legend2)
    set_topics_as_ticks_to_axis(fig=fig, ax=ax, extrawidth=0.4)
    save_my_figures(f"agreement_ruffly_dots", bbox_extra_artists=[legend2, legend_FULLMOD], fig=fig)
    fig.show()


if __name__ == '__main__':
    run_get_coding_categories()
    # fig, ax, xx, reference_order, legend_entry4 = get_coding_categories(limit_to=CODING_CATEGORIES.OPERATIONMODLESS, fig=None,
    #                                                                     ax=None, reference_order=None)