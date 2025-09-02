from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.statistical_settings import alpha

# task_evaluation:
from src.task_evaluation.statistic_box_plot import get_statistik

get_statistik("switch_amount", alpha=alpha)
get_statistik("times", alpha=alpha)
from src.task_evaluation.overview_difficulty_tasks import overview_difficulty_tasks
overview_difficulty_tasks()


#demographics:
from src.demographics import get_demographic_distribution
get_demographic_distribution("gender")
get_demographic_distribution("leftHandedOrRightHanded")
get_demographic_distribution("age", False)
from src.demographics_laender import demographics_laender
demographics_laender()



from src.task_evaluation.statistic_box_plot import get_statistik
get_statistik("switch_amount",alpha=alpha)
get_statistik("times",alpha=alpha)


from src.coding.modalities.time_needed_modalities import time_needed_modalities
from src.coding.modalities.time_needed_modalities_statistik import time_needed_modalities_statistik
time_needed_modalities()#1st
time_needed_modalities_statistik()#2nd

from coding.getting_coding_categories import run_get_coding_categories
run_get_coding_categories()

from src.task_evaluation.overview_difficulty_tasks import overview_difficulty_tasks
overview_difficulty_tasks()

from src.coding.category_table.table_choice.table_operation_choice import get_table_operation_choice
get_table_operation_choice(CODING_CATEGORIES.OPERATIONMODLESS)
get_table_operation_choice(CODING_CATEGORIES.LOCATIONMODLESS)

from src.coding.modalities.combined_modalities import run_combined_modalities
from src.coding.modalities.one_modality import plot_one_modality
try:
    plot_one_modality()
except:
    pass # not all p coded
run_combined_modalities()

from src.languages.mother_language import mother_language
mother_language()

