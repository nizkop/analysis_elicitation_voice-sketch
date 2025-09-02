from enum import Enum


class TaskJsonKind(Enum):
    INFO = 0
    SKIPPED = 1
    QUESTION = 2
    CODES = 3
    CODESconsistency = 4
