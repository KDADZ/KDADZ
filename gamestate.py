import enum

class GameState(enum.Enum):
    
    MENU = 1
    MID_LEVEL = 2
    TRIVIA_ROOM = 3
    SHOPKEEPER = 4
    WIN = 5
    LOSE = 6
    VICTORY = 7
    SHOP = 8
    INVENTORY = 9
    CREDITS_SCENE = 10