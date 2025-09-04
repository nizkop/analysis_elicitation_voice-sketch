import json
import os
from enum import Enum

from help_scripts import known_errors_json
from src.TaskJsonKind import TaskJsonKind


class Language(Enum):
    DE = "de"
    EN = "en"
    IS = "is"


demographic_options = {
  "gender": ["male", "female", "non-binary"],
  "age": ["18-29", "30-39", "40-49", "50-59", "60-69", r">70"],
  "leftHandedOrRightHanded": ["left", "right"],
  "nativeLanguage": [],
  "anyExperienceVoice": ["none", "a little", "a lot"],
  "anyExperiencePen": ["none", "a little", "a lot"],
  "anyExperienceTablet": ["none", "a little", "a lot"],
  "anyExperienceSpreadsheet": ["none", "a little", "a lot"],
}


class participant:
    def __init__(self, id: int, language:Language, living_in: Language):
        if len(str(id)) == 3:
            self.id = str(id)
        elif len(str(id)) == 2:
            self.id = f"0{id}"
        elif len(str(id)) == 1:
            self.id = f"00{id}"
        else:
            self.id = f"{id}"
        self.language = language
        self.living_in = living_in
        self.demographics_file_name = "21_demographics.json"

    def get_folder(self, infokind: TaskJsonKind):
        if infokind == TaskJsonKind.CODES:
            return f"./Participant_data/Participant_{self.id}/CODES/"
        elif infokind == TaskJsonKind.CODESconsistency:
            return f"./Participant_data/Participant_{self.id}/CODES_duplicate/"
        return f"./Participant_data/Participant_{self.id}/DATA/"

    def get_demographics(self):
        file_path = os.path.join(self.get_folder(infokind=TaskJsonKind.INFO), self.demographics_file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data
                except json.JSONDecodeError as e:
                    if file_path not in known_errors_json and p.id != "000":
                        raise Exception(f"Fehler beim Laden von participants data {file_path}: {e}")
        else:
            print("P not existing", file_path)

    def get_possible_questionnaire_names(self):
        for no in range(1,21):
            for task_id in range(1,21):
                file_name = f"{no}_questionnaire_task{task_id}.json"



p0 = participant("000", Language.EN, living_in = Language.DE)
# grep "chosenlanguage" Participant_*/DATA/21_demographics.json

participants = [
    #GERMAN:
    p0,
    # ICELANDIC:
]