from src.participants import Language


class PureModalityTiming():
    def __init__(self, task_id:str, task_topic:str, task_group:str, modality: str, time_in_s:float, language:Language, solution_index:int):
        if modality not in ["sketch", "voice"]:
            raise Exception("wrong modality")
        self.task_id = task_id
        self.task_topic = task_topic
        self.task_group = task_group
        self.solution_Index = solution_index

        self.modality = modality
        self.time_in_s = time_in_s
        self.language = language