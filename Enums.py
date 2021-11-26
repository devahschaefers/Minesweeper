from enum import Enum

class Placement(Enum):
    TOPLEFT = 1
    TOPRIGHT = 2
    BOTTOMRIGHT = 3
    BOTTOMLEFT = 4
    CENTER = 5

class GameState(Enum):
    PLAYING = 1
    LOST = 2
    WON = 3
