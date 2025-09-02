import pandas as pd

from src.Tasks.Task import tasks
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.getting_coding_categories import get_categories_for_tasks
from src.Tasks.task_topic import TaskTopic


def get_category_table_of_selected_tasks(task_topic: TaskTopic, limit_to:CODING_CATEGORIES):
    try:
        coding_data, info_dict, task_names = get_categories_for_tasks(
            [i for i in tasks if i.identifier in task_topic.value ],
            limit_to=limit_to
        )

        # 1. Sammle alle Kategorien aus allen Tasks
        all_categories = sorted({
            category
            for task_data in info_dict.values()
            for category in task_data.keys()
        })
        if not all_categories:
            print(f"keine Kategorien für {task_topic} mit {limit_to=}")
            return pd.DataFrame()

        # 2. Baue eine Tabelle mit Häufigkeiten ("" statt 0)
        table_data = []
        task_ids = []

        number_of_categories_per_task = {}
        for task_id, task_data in info_dict.items():
            row = [
                len(task_data.get(category, [])) if category in task_data else ""
                for category in all_categories
            ]
            row = [value if value != 0 else "" for value in row]
            table_data.append(row)
            task_ids.append(f"task {task_id}")
            number_of_categories_per_task[task_id] = len([i for i in row if isinstance(i, int) and i != 0 ])

        df = pd.DataFrame(table_data, columns=all_categories, index=task_ids)

        # 3. Summenzeile hinzufügen
        df_numeric = df.replace("", 0).astype(float)  # Temporär Strings zu 0
        sum_row = df_numeric.sum(axis=0)
        sum_row = sum_row.replace(0, "")
        df.loc["total number of occurences"] = sum_row
        all_solutions = sum(df.loc["total number of occurences"])
        df.loc["% of occurences"] = float(100) * sum_row / float(all_solutions)

        df = df.transpose()  # Zeilen <-> Spalten tauschen
        # task_cols = [col for col in df.columns if col.startswith('task')]
        # df_tasks = df[task_cols]
        # df_numeric = df_tasks.apply(pd.to_numeric, errors='coerce').fillna(0)
        # df_percent = df_numeric.apply(lambda x: 100 * x / x.sum(), axis=0)
        df.to_csv(f"kategorie_tasks{task_topic.name}_tabelle_{limit_to.name}.csv", sep=";", index=True, float_format="%.1f")
        return df, number_of_categories_per_task
    except Exception as e:
        print("failed", e)
        raise Exception(e)
        return None
