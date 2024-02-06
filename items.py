class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

def heal_effect(player, amount):
    player.heal(amount)

def redo_effect(game):
    game.allow_redo()

def double_points_effect(game):
    game.double_points_this_round()

def skip_round_effect(game):
    game.skip_round()

def win_game_effect(game):
    game.win_condition_met()

# Defining the items
red_potion = Item("Red Potion", lambda player: heal_effect(player, 2))
redo_card = Item("Redo Card", lambda game: redo_effect(game))
sock = Item("Sock", lambda game: win_game_effect(game))
double_point_card = Item("Double Point Card", lambda game: double_points_effect(game))
skipped = Item("Skipped!", lambda game: skip_round_effect(game))
