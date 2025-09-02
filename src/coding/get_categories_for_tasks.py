from src.Tasks.Task import Task
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.agreement_rate import agreement_rate
from src.coding.check_category_for_duplicates import check_category_for_duplicates
from src.coding.get_modality_free_category import get_modality_free_category
from src.participants import participants


def get_categories_for_tasks(tasks:list[Task], limit_to:CODING_CATEGORIES):
    # print("get_categories_for_tasks", tasks, limit_to)
    task_names = []
    agreement_rates = []
    information_about_agreement_rate = {}
    coding_data = []
    for task_idx, task in enumerate(tasks):
        if task.get_group() != "P":
            categories = {}
            p_of_categories = {}
            for p in participants:
                if task.coded(p=p):
                    category_array = task.get_category(p=p)
                    if category_array is not None and len(category_array) > 0:
                        for category in category_array:
                            if len(category.replace(" ","")) == 0:
                                raise Exception("empty category")
                            if category is not None or len(category.replace(" ","")) == 0:
                                category = get_modality_free_category(category, limit_to=limit_to)
                                if category is not None:
                                    check_category_for_duplicates(category, info=f"p {p.id}, task {task.identifier}")
                                    if category in categories:
                                        categories[category] += 1
                                        p_of_categories[category].append(f"p{p.id}")
                                    else:
                                        categories[category] = 1
                                        p_of_categories[category] = [f"p{p.id}"]
                            else:
                                raise Exception("no category")
                    # else:
                    #     try:
                    #         categories["skipped/missunderstood"] += 1
                    #     except:
                    #         categories["skipped/missunderstood"] = 1

                else:
                    print("no codes: participant", p.id, "task", task.identifier)

            categories = dict(sorted(categories.items()))#alphabetic ordering
            print("\nTask:", task.identifier, "-> uses categories:")

            a = agreement_rate(categories, information=p_of_categories)
            new_data_item = {"task_name": str(task.identifier),
                             "agreement_rate": a,
                             "group": task.get_group()
                             }
            coding_data.append(new_data_item)
            agreement_rates.append(a)
            task_names.append(str(task.identifier))
            print("-> agreement:", a)
            print()
            information_about_agreement_rate[task.identifier] = p_of_categories


    # plt.plot(agreement_rates)
    # plt.show()
    # plt.close()
    return coding_data, information_about_agreement_rate, task_names
