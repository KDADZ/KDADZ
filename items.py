class Item:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description

red_potion = Item("Health Potion", 500, "Restores health")
redo_potion = Item("Redo Potion", 800, "Allows redoing a question")
magic_sock = Item("Magic Sock", 1500, "Ends the game with a win")

