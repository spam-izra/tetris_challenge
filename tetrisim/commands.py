from enum import Enum

class Command(Enum):
    PASS             = "P"
    SOFT_SPEEDUP     = "S"
    HARD_SPEEDUP     = "H"
    LEFT             = "L"
    RIGHT            = "R"
    CLOCKWISE        = "F"
    COUNTERCLOCKWISE = "B"
