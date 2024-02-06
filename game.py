import pygame
from player import Player
from items import red_potion
from trivia_room import TriviaRoom
from gamestate import GameState
from menu import Menu
from lose_screen import LoseScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Trivia Roguelite Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.menu = Menu(self)

        self.player = Player(10, 100)
        self.player.add_item(red_potion, 1)
        self.trivia_room_instance = None

        self.lose_screen = LoseScreen(self.screen)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            # Simulation for lose screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:  # Press 'L' key to simulate losing
                    self.transition_state(GameState.LOSE)

            if self.current_state == GameState.MENU:
                self.menu.handle_events(events)
            elif self.current_state == GameState.LOSE:
                self.lose_screen.handle_event(event, self.transition_state)

    def update(self):
        if self.current_state == GameState.MID_LEVEL:
            # Update logic for mid-level
            pass
        elif self.current_state == GameState.TRIVIA_ROOM:
            # Update logic for trivia room
            pass
        if self.current_state == GameState.LOSE:
        # Update logic for lose screen if needed
            pass

    def render(self):
        if self.current_state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.draw(mouse_pos)
            pass
        elif self.current_state == GameState.TRIVIA_ROOM:
            # Rendering for trivia room
            pass
        elif self.current_state == GameState.LOSE:
            mouse_pos = pygame.mouse.get_pos()
            self.lose_screen.draw(mouse_pos)

        pygame.display.flip()
        
    def trivia_room(self, selected_category):
        if not trivia_room_instance:
            trivia_room_instance = TriviaRoom(game, selected_category)
        else:
            trivia_room_instance.category = selected_category
            trivia_room_instance.load_new_question()
            
    def transition_state(self, new_state):
        self.current_state = new_state
        # Handle any setup needed for the new state
        if new_state == GameState.TRIVIA_ROOM:
            # Example: set up player position for trivia room
            self.player.transition_to_state("trivia_room", new_position=(100, 500))  # Just an example
        elif new_state == GameState.MID_LEVEL:
            # Setup for returning to mid-level
            self.player.transition_to_state("mid_level")
        elif new_state == GameState.MENU:
        # If specific setup is required when returning to the menu, do it here
        # For example, reset game progress, scores, etc., if the game starts anew from the menu
            pass
        elif new_state == GameState.LOSE:
        # If there's any specific setup when entering the lose screen, do it here
        # Often there might not be much to do except showing the lose screen
            pass

        
    def allow_redo(self):
        pass
    
    def skip_round(self):
        pass
    
    def trivia_room_logic():
        pass

game = Game()

