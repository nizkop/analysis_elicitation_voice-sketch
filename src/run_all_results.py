from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.statistical_settings import alpha

# task_evaluation:
from src.task_evaluation.statistic_box_plot import get_statistik

try:
    get_statistik("switch_amount", alpha=alpha)
    get_statistik("times", alpha=alpha)
except:
    pass
from src.task_evaluation.overview_difficulty_tasks import overview_difficulty_tasks

try:
    overview_difficulty_tasks()
except:
    pass


#demographics:
from src.demographics import get_demographic_distribution
try:
    get_demographic_distribution("gender")
    get_demographic_distribution("leftHandedOrRightHanded")
    get_demographic_distribution("age", False)
except:
    pass

from src.demographics_laender import demographics_laender
try:
    demographics_laender()
except:
    pass


from src.task_evaluation.statistic_box_plot import get_statistik
try:
    get_statistik("switch_amount",alpha=alpha)
    get_statistik("times",alpha=alpha)
except:
    pass


from src.coding.modalities.time_needed_modalities import time_needed_modalities
from src.coding.modalities.time_needed_modalities_statistik import time_needed_modalities_statistik
try:
    time_needed_modalities()#1st
    time_needed_modalities_statistik()#2nd
except:
    pass

from src.coding.getting_coding_categories import run_get_coding_categories
try:
    run_get_coding_categories()
except:
    pass

from src.task_evaluation.overview_difficulty_tasks import overview_difficulty_tasks
try:
    overview_difficulty_tasks()
except:
    pass

from src.coding.category_table.table_choice.table_operation_choice import get_table_operation_choice
try:
    get_table_operation_choice(CODING_CATEGORIES.OPERATIONMODLESS)
    get_table_operation_choice(CODING_CATEGORIES.LOCATIONMODLESS)
except:
    pass

from src.coding.modalities.combined_modalities import run_combined_modalities
from src.coding.modalities.one_modality import plot_one_modality
try:
    plot_one_modality()
except:
    pass # not all p coded
try:
    run_combined_modalities()
except:
    pass

from src.languages.mother_language import mother_language
try:
    mother_language()
except:
    pass

