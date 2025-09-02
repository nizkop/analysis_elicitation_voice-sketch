from enum import Enum


class CODING_CATEGORIES(Enum):
    FULLMODLESS = "Full/No-Mod"
    FULLMOD = "Full/Mod"
    OPERATIONMODLESS = "Operation/No-Mod"
    LOCATIONMODLESS = "Location/No-Mod"
    LOCATIONMOD = "Location/Mod"
    OPERATIONMOD = "Operation/Mod"
    EMPTYMOD = "Empty/Mod"