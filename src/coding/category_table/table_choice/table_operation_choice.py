from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.category_table.table_choice.convert_table_into_relative_values import convert_table_into_relative_values
from src.coding.category_table.table_choice.plot_operation_relative_values_with_lines import \
    plot_operation_relative_values_with_lines
from src.coding.category_table.table_choice.table_operation_choice_absolute import table_operation_choice_absolute





def get_table_operation_choice(coding_category:CODING_CATEGORIES):
    if coding_category == CODING_CATEGORIES.OPERATIONMODLESS:
        file_name = "operation_choice"
    elif coding_category == CODING_CATEGORIES.LOCATIONMODLESS:
        file_name = "location_choice"
    else:
        raise Exception("get_table_operation_choice: choose other category")
    amount_of_tasks_per_topic = table_operation_choice_absolute(file_name, coding_category=coding_category)
    df = convert_table_into_relative_values(file_name)
    plot_operation_relative_values_with_lines(filename=file_name, df_percent=df,
                                              coding_category=coding_category,
                                              amount_of_tasks_per_topic=amount_of_tasks_per_topic)


if __name__ == "__main__":
    get_table_operation_choice(CODING_CATEGORIES.OPERATIONMODLESS)
    get_table_operation_choice(CODING_CATEGORIES.LOCATIONMODLESS)
