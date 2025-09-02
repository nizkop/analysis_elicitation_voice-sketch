from enum import Enum


class TaskTopic(Enum):
    CALCULATION = ["4", "8", "17", "18", "20"]
    FORMATTING = ["9", "10", "19", "13"]
    EDITING = ["1", "14", "15",
               "2", "3", "6" ]
    STRUCTURECHANGE = [ "7", "E", "16"]

    def get_info_from_task_topic(self):
        # Gibt einfach den Enum-Namen in Kleinbuchstaben zurück
        if self.name == "STRUCTURECHANGE":
            return "Structure Change"
        return self.name[0].upper() + self.name.lower()[1:]

    def order(self):
        self.FORMATTING
        self.EDITING
        self.STRUCTURECHANGE
        self.CALCULATION


topic_order = [TaskTopic.FORMATTING, TaskTopic.EDITING, TaskTopic.STRUCTURECHANGE, TaskTopic.CALCULATION]#order as in report!
topic_order_dict = {topic_order[i]: i for i in range(len(topic_order))}