class Inventory:
    def __init__(self):
        self.items = {}
        
    def add_item(self, item_name, quantity):
        
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
            
    def remove_item(self, item_name, quantity=1):
        
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]
            return True
        return False

    def use_item(self, item_name, player, game):
        if item_name in self.items and self.items[item_name][1] > 0:
            item, quantity = self.items[item_name]
            item.effect(player, game)
            self.items[item_name][1] -= 1
            if self.items[item_name][1] == 0:
                del self.items[item_name]