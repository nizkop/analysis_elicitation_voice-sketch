
import os
import pandas as pd

from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.get_category_table_of_selected_tasks import get_category_table_of_selected_tasks
from src.Tasks.task_topic import  topic_order


def table_operation_choice_absolute(file_name:str, coding_category:CODING_CATEGORIES):
    """
    write table of total amount of operation categories into csv
    :return:
    """
    try:
        os.remove(file_name+".csv")
    except:
        pass
    mode = "w"
    amount_of_tasks_per_topic = []
    for topic in topic_order:
        df, number_of_categories_per_task = get_category_table_of_selected_tasks(task_topic=topic, limit_to=coding_category)
        df = df.drop("total number of occurences", axis=1, errors='ignore').drop("% of occurences", axis=1, errors='ignore')
        df_transposed = df.T
        df_transposed.insert(0, "task_topic", topic.name)
        df_transposed = df_transposed.reset_index().rename(columns={"index": "Task"})
        if coding_category == CODING_CATEGORIES.OPERATIONMODLESS:
            try:
                df_transposed = df_transposed[["task_topic", "Task",
                                           "operation:words", 'operation:symbol - operation:words', "operation:symbol"] ]
            except:
                df_transposed = df_transposed[["task_topic", "Task",
                                               "operation:words", 'operation:words - operation:symbol', "operation:symbol"]]
        else:
            print(df_transposed.index.tolist())
            df_transposed = df_transposed[["task_topic", "Task"] + [col for col in df_transposed.columns if col not in ["task_topic", "Task"]]]

        if mode == "w":
            df_combined = df_transposed
        else:
            df_combined = pd.concat([df_combined, df_transposed], ignore_index=True)
        amount_of_tasks_per_topic += [df_transposed.shape[0]]
        mode = "a"
    df_combined.to_csv(file_name + ".csv", mode=mode, sep=";",
                       header="w",  # True if mode == "w" else False,
                       index=False)
    return amount_of_tasks_per_topic