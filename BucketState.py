from enum import Enum

class BucketState(Enum):
    ONE_IN_FROM_LEFT = 0
    ONE_IN_FROM_RIGHT = 1
    ONE_OUT_TO_LEFT = 2
    ONE_OUT_TO_RIGHT = 3
    TWO_IN = 4
    UNKNOWN = 5
