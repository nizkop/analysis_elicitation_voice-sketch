from src.plt_settings import size_2


def create_topic_axis(fig, ax_main, topics_with_x_values, extrawidth:float):
    pos_main = ax_main.get_position()
    left = pos_main.x0
    width = pos_main.width
    bottom = pos_main.y1  # genau oberhalb von ax_main
    ax_topic = fig.add_axes([left, bottom, width, 0.008])

    topic_intervals = []
    max_x = 0
    for topic, x_values in topics_with_x_values.items():
        start = min(x_values)
        end = max(x_values)
        topic_intervals.append((start-extrawidth, end+extrawidth))
        max_x = max(max_x, max(x_values))

    for (start, end) in topic_intervals:
        ax_topic.axvspan(start, end, color="black", alpha=1)

    ax_topic.set_xlim(ax_main.get_xlim())
    ax_topic.tick_params(labelbottom=False, labeltop=True)
    ax_topic.set_yticks([])

    for spine in ax_topic.spines.values():
        spine.set_visible(False)
    ax_topic.tick_params(axis='x', which='both', length=0)

    ax_topic.xaxis.set_label_position('top')
    ax_topic.xaxis.tick_top()
    ax_topic.set_xticks([(start + end) / 2 for start, end in topic_intervals])
    ax_topic.set_xticklabels(topics_with_x_values.keys(), ha='center')

    return ax_topic

