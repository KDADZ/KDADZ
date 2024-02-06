import pygame
from player import Player
from items import red_potion
from trivia_room import TriviaRoom

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Trivia Roguelite Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(10, 100)
        self.player.add_item(red_potion, 1)
        self.trivia_room_instance = None

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Add more event handling here (e.g., key presses, mouse clicks)

    def update(self):
        # Update game state, player, and other components
        pass

    def render(self):
        self.screen.fill((0, 50, 50))  # Clear the screen with black
        # Add rendering code here (draw player, items, UI elements)
        pygame.display.flip()  # Update the full display Surface to the screen
        
    def trivia_room(self, selected_category):
        
        if not trivia_room_instance:
            trivia_room_instance = TriviaRoom(game, selected_category)
        else:
            trivia_room_instance.category = selected_category
            trivia_room_instance.load_new_question()
        
    def allow_redo(self):
        pass
    
    def skip_round(self):
        pass

game = Game()

