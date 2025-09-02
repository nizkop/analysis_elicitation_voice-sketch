from src.Tasks.Task import Task
from src.TaskJsonKind import TaskJsonKind
from src.coding.check_category_for_duplicates import check_category_for_duplicates
from src.participants import participants


def get_voice_commands_for_task(taskid):
    task = Task(taskid)
    for p in participants:
        categories = task.get_category(p=p)
        for category in categories:
            check_category_for_duplicates(category, info=f"p {p.id}, task {task.identifier}")
            if "voice" in category:
                data = task.get_dictionary(p=p, infokind=TaskJsonKind.INFO)
                if data is not None:
                    result = remove_added_info_in_brackets(data["taskData"]["voice"])
                    result = remove_added_info_in_brackets_2(result)
                    print(f"p{p.id}:\t", result.strip(), "\t->\t", category)


def remove_added_info_in_brackets(s:str, bracket_kind="("):
    if not( "(" in s and ")" in s ):
        return s
    start = s.find("(")
    end = s.find(")", start)
    new_s = s[:start] + s[end + 1:]
    return remove_added_info_in_brackets(new_s)

def remove_added_info_in_brackets_2(s:str):
    if not( "[" in s and "]" in s ):
        return s
    start = s.find("[")
    end = s.find("]", start)
    new_s = s[:start] + s[end + 1:]
    return remove_added_info_in_brackets(new_s)

if __name__ == '__main__':
    # print( remove_added_info_in_brackets("Dies ist ein (test) string.mit mehreen () (Klammern)") )
    get_voice_commands_for_task(taskid = "1")

