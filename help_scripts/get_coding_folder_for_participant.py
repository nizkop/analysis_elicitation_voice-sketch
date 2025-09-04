import json
import os

from src.Tasks.Task import tasks
from src.TaskJsonKind import TaskJsonKind


def get_coding_folder_for_participant(id: int, kind: TaskJsonKind = TaskJsonKind.CODES):
    data =  {
         "OPERATION": {
            "SYMBOL": None,
            "EXAMPLE": None,
            "KNOWLEDGE": None,
            "WORDS": None
         },
         "LOCATION": {
            "SELECTION": None,
            "ADDRESS": None,
            "ENTRY": None,
            "POSITION": None,
            "KNOWLEDGE": None,
            "CONNECTED-ANNOTATION": None
         },
         "GUI": None
     }

    dir = 'CODES_duplicate' if kind == TaskJsonKind.CODESconsistency else 'CODES'
    # os.mkdir(f"Participant_data/Participant_{id}/{dir}")

    for task in tasks:
        if task.get_group() != "P":
            with open(f"Participant_data/Participant_{id}/{dir}/coding_task_{task.identifier}.json", "w") as f:
                json.dump(data, f, indent=4)


if __name__ == "__main__":
    for i in range(0,1):
        get_coding_folder_for_participant(id=i, kind = TaskJsonKind.CODES)