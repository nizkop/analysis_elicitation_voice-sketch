from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.get_category_table_of_selected_tasks import get_category_table_of_selected_tasks
from src.Tasks.task_topic import TaskTopic

#Mathematics: ["4", "8", "17", "18", "20"]
# df = get_category_table_of_selected_tasks(task_topic=task_ids, limit_to = CODING_CATEGORIES.LOCATION, info=info)
# df = get_category_table_of_selected_tasks(task_topic=TaskTopic.CALCULATION, limit_to = CODING_CATEGORIES.OPERATION_MODLESS)



# #Formatting and Visualization}
# task_ids = ["9", "10", "19", "13"]
# info="formatting"
# # df = get_category_table_of_selected_tasks(task_topic=task_ids, limit_to = CODING_CATEGORIES.LOCATION, info=info)
# df = get_category_table_of_selected_tasks(task_topic=TaskTopic.FORMATTING, limit_to = CODING_CATEGORIES.OPERATION, info=info)
#
# #Data Edit/series
# task_ids = ["1", "14", "15"]
# info="edit"
# # df = get_category_table_of_selected_tasks(task_topic=task_ids, limit_to = CODING_CATEGORIES.LOCATION, info=info)
# df = get_category_table_of_selected_tasks(task_topic=TaskTopic.EDIT, limit_to = CODING_CATEGORIES.OPERATION, info=info)
#
# #Structure Change: moving/sorting + deletion

# df = get_category_table_of_selected_tasks(task_ids, limit_to = CODING_CATEGORIES.LOCATION, info=info)
df = get_category_table_of_selected_tasks(task_topic=TaskTopic.EDITING, limit_to = CODING_CATEGORIES.FULLMOD)
