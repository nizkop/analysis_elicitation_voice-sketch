
from src.Tasks.Task import tasks
from src.Tasks.create_topic_axis import create_topic_axis
from src.Tasks.task_topic import topic_order


def get_tasks_in_topic():
    tasks_along_topics = []
    for topic in topic_order:
        for task in tasks:
            if task.topic.value == topic.value:
                tasks_along_topics.append(task)
    return tasks_along_topics


def amounts_of_tasks_per_topic():
    amounts = {}
    for topic in topic_order:
        amounts[topic] = len(topic.value)
    return amounts

def get_xvalues_of_topic() -> dict:
    x_werte_topic = {}
    tasks = get_tasks_in_topic()
    for i in range(len(tasks)):
        task = tasks[i]
        if task.topic.get_info_from_task_topic() in x_werte_topic.keys():
            x_werte_topic[task.topic.get_info_from_task_topic()].append(i)
        else:
            x_werte_topic[task.topic.get_info_from_task_topic()] = [i]
    return x_werte_topic


def set_topics_as_ticks_to_axis(fig, ax, extrawidth:float):
    topics_with_x_values = get_xvalues_of_topic()
    create_topic_axis(fig=fig, ax_main=ax, topics_with_x_values= topics_with_x_values, extrawidth=extrawidth)



if __name__ == '__main__':
    print(amounts_of_tasks_per_topic())
    print(get_xvalues_of_topic())