from enum import Enum


class QuestionnaireOption(Enum):
    answer1 = "very easy"
    answer2 = "easy"
    answer3 = "neutral"
    answer4 = "difficult"
    answer5 = "very difficult"
    skipped = "skipped/missunderstood"



# print(color_mapping_QuestionnaireOptions)