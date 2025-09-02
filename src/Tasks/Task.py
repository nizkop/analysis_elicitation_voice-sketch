import json
import os
from datetime import datetime
from typing import List

from help_scripts.known_errors_json import known_errors_json
from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.check_category_for_duplicates import check_category_for_duplicates
from src.participants import participant
from src.TaskJsonKind import TaskJsonKind
from src.coding.Coding import Coding
from src.Tasks.task_topic import TaskTopic


class Task:

    def __init__(self, identifier:str):
        self.identifier = identifier # picture_file_name_without_file_format.replace("task_","").replace("Task_","")
        self.picture_file_name = f"Task_{identifier}.png"
        self.picture_file = f"Task_{identifier}"


        self.difficulty_question = "answer1"
        self.perceived_difficulty = {
            # list of participant ids per answer
        }
        self.group_P = ["C", "G"]
        self.group_A = ["1","2","3", "4","6","7"]
        self.group_B = ["8","9","10", "E","14","15"]
        self.group_C = ["13","16","17", "18","19","20"]

        self.topic = next((topic for topic in TaskTopic if identifier in topic.value), None)


        self.info_file_name = f"Task_{self.identifier}.json"
        self.skipped_file_name = f"Task_{self.identifier}_Skipped.json"
        self.questionnaire_file_name = f"questionnaire_task_{self.identifier}.json"
        self.code_file_name = f"coding_task_{identifier}.json"


    def get_group(self):
        if self.identifier in self.group_P:
            return "P"
        if self.identifier in self.group_A:
            return "A"
        if self.identifier in self.group_B:
            return "B"
        if self.identifier in self.group_C:
            return "C"
        return None

    def get_possible_number(self) -> List[int]:
        if self.identifier.lower() == "c":
            return [1]
        if self.identifier.lower() == "g":
            return [2]
        if self.identifier in self.group_A:
            return [3,4,5,6,7,8]
        if self.identifier in self.group_B:
            return [9,10,11,12,13,14]
        if self.identifier in self.group_C:
            return [15,16,17,18,19,20]
        return []

    def skipped(self, p:participant) -> bool:
        file_path = os.path.join(p.get_folder(infokind=TaskJsonKind.SKIPPED), self.skipped_file_name)
        return os.path.isfile(file_path)

    def missunderstood(self, p:participant) -> bool:
        if self.skipped(p):
            return False
        file_path = os.path.join(p.get_folder(infokind=TaskJsonKind.INFO), self.info_file_name)
        return file_path in known_errors_json

    def coded(self, p:participant) -> bool:
        # data = self.get_dictionary(p=p, infokind=TaskJsonKind.INFO)
        # if data is None:
        #     return self.skipped(p=p)
        # matching_keys = [key for key in data.keys() if re.fullmatch(r"codes\d*", key)] # 0 or more numbers behind "codes"
        # if len(matching_keys) == 0:
        #     return False
        # if Coding(data["codes"]).test_array_empty():
        #     return False
        return len(self.get_coding(p=p)) > 0


    def get_coding(self, p:participant, infokind:TaskJsonKind=TaskJsonKind.CODES) -> List[dict]:
        if infokind not in [TaskJsonKind.CODES, TaskJsonKind.CODESconsistency]:
            raise Exception("get_coding: invalid infokind")
        code_solutions = self.get_dictionary(p=p, infokind=infokind)
        if code_solutions is None:
            if self.skipped(p=p):
                return [{"SKIPPED": True}]
            else:
                return []
        if not isinstance(code_solutions, list):
            raise Exception("")

        codes = []
        for code in code_solutions:
            if code is not None and not Coding(code).test_array_empty():
                codes.append(code)
            # else:
            #     print("\tnot added because", code is not None, not Coding(code).test_array_empty())
            #     print("\t", code)
        return codes

    def get_category(self, p: participant, infokind:TaskJsonKind=TaskJsonKind.CODES) -> List[str]:
        if ( not self.coded(p=p) ) or self.missunderstood(p=p) or self.skipped(p=p):
            return ["SKIPPED"]
        codes = self.get_coding(p=p, infokind=infokind)
        categories = []
        for code in codes:
            category = Coding(code).get_category()
            check_category_for_duplicates(category, info=f"Task, p {p.id}, task {self.identifier}")
            knowledge_free_category_parts = []
            for part in category.split(" - "):
                if "KNOWLEDGE".lower() in part.lower():# or "knowledge" in part.lower():
                    continue
                if "EXAMPLE".lower() in part.lower():
                    if not "SYMBOL".lower() in part.lower():
                        raise Exception(f"are you sure? Example, but no symbol! p {p.id}, task {self.identifier}")
                    continue
                part = part.replace("POSITION", "POINTING")
                part = part.replace("SELECTION", "POINTING")
                if "sketchlocation" in part:
                    raise Exception()
                knowledge_free_category_parts.append(part)
            category = ' - '.join(
                set(knowledge_free_category_parts)
            )
            categories.append( category )

        #testing validity:
        for test_category in categories:
            if (test_category is not None) and (not "gui" in test_category.lower()) and (len(test_category) > 0):
                if "location" not in test_category.lower():# and "knowledge" not in test_category.lower():
                    raise Exception(f"No location found: task {self.identifier}, p {p.id} by {test_category.lower()}")
                if "operation" not in test_category.lower():# and "knowledge" not in test_category.lower():
                    raise Exception(f"No operation found: task {self.identifier}, p {p.id} by {test_category.lower()}")
        # test:
        for i in categories:
            if "knowledge" in i.lower():
                raise Exception("KNOWLEDGE nicht gefiltert")
            if "example" in i.lower():
                raise Exception("EXAMPLE nicht gefiltert")
        return categories




    def get_dictionary(self, p:participant, infokind: TaskJsonKind) -> dict:
        if infokind == TaskJsonKind.INFO:
            file_name = self.info_file_name
        elif infokind == TaskJsonKind.SKIPPED:
            file_name = self.skipped_file_name
        elif infokind == TaskJsonKind.QUESTION:
            file_name = self.questionnaire_file_name
        elif infokind == TaskJsonKind.CODES or infokind == TaskJsonKind.CODESconsistency:
            file_name = self.code_file_name

        file_path = os.path.join(p.get_folder(infokind=infokind), file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if infokind == TaskJsonKind.QUESTION or infokind == TaskJsonKind.SKIPPED:
                        if data["picture_file_name"].lower() == self.picture_file_name.lower():
                            return data
                        else:
                            raise Exception(f"data wrong {file_path}")
                    elif infokind == TaskJsonKind.INFO:
                        taskData = data["taskData"]
                        if taskData["picture_file_name"].lower() == self.picture_file_name.lower():
                            return data
                        elif file_path not in known_errors_json:
                            raise Exception(f"data wrong {file_path}")
                    elif infokind == TaskJsonKind.CODES or infokind == TaskJsonKind.CODESconsistency:
                        if isinstance(data, list):
                            return data
                        return [data]
                    else:
                        raise Exception(f"unknown handling of infokind for reading data from json {infokind.value}")
                except json.JSONDecodeError as e:
                    if file_path not in known_errors_json and p.id != "000":
                        raise Exception(f"Fehler beim Laden von {[file_path]}: {e}")
        elif file_path not in known_errors_json and self.get_group() != "P":
            print("Task not existing", file_path)


    def median_watching_time(self, participants: List[participant]) -> float:
        total_time = []
        for p in participants:
            data = self.get_dictionary(p, infokind=TaskJsonKind.INFO)
            if data is not None and not ( self.skipped(p) or self.missunderstood(p) ):
                endTimeWatching = data["taskData"]["endTimeWatching"]
                startTimeWatching = data["taskData"]["startTimeWatching"]
                start = datetime.strptime(startTimeWatching, "%Y-%m-%dT%H:%M:%S.%fZ")
                end = datetime.strptime(endTimeWatching, "%Y-%m-%dT%H:%M:%S.%fZ")
                diff = end - start
                total_time.append( diff.total_seconds() )

        return total_time#, median(total_time), np.percentile(total_time, 75) - np.percentile(total_time, 25)

    def get_switch_median(self, participants: List[participant]) -> float:
        switches = []
        for p in participants:
            data = self.get_dictionary(p, infokind=TaskJsonKind.INFO)
            if data is not None and not ( self.skipped(p) or self.missunderstood(p) ):
                amount_of_sheet2_clicks = data["taskData"]["switchNumber"]
                if amount_of_sheet2_clicks == 0:
                    # can happen if task has hint!
                    print(f"\033[31mtasks not viewed: {self.identifier}, participant {p.id}\033[0m")
                    # raise Exception(f"")
                switches.append(amount_of_sheet2_clicks)
        return switches# median(switches), np.percentile(switches, 75) - np.percentile(switches, 25)


task_picture_numbers = [
    # "C", "G",
    "1", "2", "3", "4", "6", "7", "8", "9", "10",
    "E", "13", "14", "15", "16", "17", "18", "19", "20"
]


tasks = []
for t in task_picture_numbers:
    tasks.append( Task(t))


# print([t.picture_file_name for t in tasks])
