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




p0 = participant("000", Language.DE, living_in = Language.DE)
p1 = participant("001", Language.DE, living_in = Language.DE)
p2 = participant("002", Language.DE, living_in = Language.DE)
p3 = participant("003", Language.DE, living_in = Language.DE)
p4 = participant("004", Language.DE, living_in = Language.DE)
p5 = participant("005", Language.DE, living_in = Language.DE)
p6 = participant("006", Language.DE, living_in = Language.DE)
p7 = participant("007", Language.DE, living_in = Language.DE)
p8 = participant("008", Language.DE, living_in = Language.DE)
p9 = participant("009", Language.DE, living_in = Language.DE)
p10 = participant("010", Language.DE, living_in = Language.DE)
p11 = participant("011", Language.DE, living_in = Language.DE)
p12 = participant("012", Language.DE, living_in = Language.DE)
p13 = participant("013", Language.DE, living_in = Language.DE)
p14 = participant("014", Language.DE, living_in = Language.DE)
p15 = participant("015", Language.DE, living_in = Language.DE)
p16 = participant("016", Language.DE, living_in = Language.DE)
p17 = participant("017", Language.DE, living_in = Language.DE)
p18 = participant("018", Language.DE, living_in = Language.DE)
p19 = participant("019", Language.DE, living_in = Language.DE)
p20 = participant("020", Language.DE, living_in = Language.DE)
p21 = participant("021", Language.DE, living_in = Language.DE)
p22 = participant("022", Language.DE, living_in = Language.DE)
p23 = participant("023", Language.DE, living_in = Language.DE)
p24 = participant("024", Language.DE, living_in = Language.DE)
p25 = participant("025", Language.DE, living_in = Language.DE)
p26 = participant("026", Language.EN, living_in = Language.DE)#DE speaking
p27 = participant("027", Language.DE, living_in = Language.DE)
p28 = participant("028", Language.DE, living_in = Language.DE)
p29 = participant("029", Language.DE, living_in = Language.DE)
p30 = participant("030", Language.DE, living_in = Language.DE)
p31 = participant("031", Language.DE, living_in = Language.DE)
p32 = participant("032", Language.DE, living_in = Language.DE)
p33 = participant("033", Language.DE, living_in = Language.DE)
# studies by valbjörn:
p101 = participant("101", Language.EN, living_in = Language.IS)#speaking english
p102 = participant("102", Language.EN, living_in = Language.IS)#speaking icelandic
p103 = participant("103", Language.EN, living_in = Language.IS)#speaking english
p104 = participant("104", Language.IS, living_in = Language.IS)#speaking icelandic (also in commands?)
p105 = participant("105", Language.EN, living_in = Language.IS)#speaking english
p106 = participant("106", Language.EN, living_in = Language.IS)#speaking english
p107 = participant("107", Language.EN, living_in = Language.IS)#speaking icelandic
p108 = participant("108", Language.EN, living_in = Language.IS)#speaking icelandic
p109 = participant("109", Language.EN, living_in = Language.IS)#speaking english
p110 = participant("110", Language.EN, living_in = Language.IS)#speaking icelandic
p111 = participant("111", Language.EN, living_in = Language.IS)#speaking icelandic
p112 = participant("112", Language.EN, living_in = Language.IS)#speaking icelandic
p113 = participant("113", Language.EN, living_in = Language.IS)#speaking icelandic
p114 = participant("114", Language.EN, living_in = Language.IS)#speaking icelandic
p115 = participant("115", Language.EN, living_in = Language.IS)#speaking icelandic (also in commands!?)
p116 = participant("116", Language.EN, living_in = Language.IS)#speaking icelandic
p117 = participant("117", Language.EN, living_in = Language.IS)#speaking icelandic


# grep "chosenlanguage" Participant_*/DATA/21_demographics.json

participants = [
    # GERMAN:
    p0,
    p1,
    p2,
    p3,
    p4,
    p5,
    p6,
    p7,
    p8,
    p9,
    p10,
    p11,
    p12,
    p13,
    p14,
    p15,
    p16,
    p17,
    p18,
    p19,
    p20,
    p21,
    p22,
    p23,
    p24,
    p25,
    p26,
    p27,
    p28,
    p29,
    p30,
    p31,
    p32,
    p33,
    # ICELANDIC:
    p101,
    p102,
    p103,
    p104,
    p105,
    p106,
    p107,
    p108,
    p109,
    p110,
    p111,
    p112,
    p113,
    p114,
    p115,
    p116,
    p117
]