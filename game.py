import pygame
from player import Player
from items import red_potion
from trivia_room import TriviaGame
from gamestate import GameState
from menu import Menu
from lose_screen import LoseScreen
from hud import HUD
from midplayer import MidLevel

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Trivia Roguelite Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.mid_level = MidLevel(self)

        self.player = Player(5, 100)  # Assuming Player initialization is correct
        self.player.add_item(red_potion, 1)  # Ensure red_potion is correctly imported
        self.trivia_room_instance = None
        self.current_level = 1

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:  # Press 'L' key to simulate losing
                    self.transition_state(GameState.LOSE)
            if self.current_state == GameState.MENU:
                self.menu.handle_events(events)
            elif self.current_state == GameState.MID_LEVEL:
                self.mid_level.handle_events(events)
            elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
                self.trivia_room_instance.handle_events(events)
            elif self.current_state == GameState.LOSE:
                self.lose_screen.handle_event(event, self.transition_state)

    def update(self):
        if self.current_state == GameState.MID_LEVEL:
            self.mid_level.update()
        elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
            self.trivia_room_instance.update()
        elif self.current_state == GameState.LOSE:
            pass  # Update logic for lose screen if needed

    def render(self):
        self.screen.fill((0, 0, 0))
        
        if self.current_state == GameState.MENU:
            mouse_pos = pygame.mouse.get_pos()
            self.menu.draw(mouse_pos)
        elif self.current_state == GameState.MID_LEVEL:
            self.mid_level.draw()
        elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
            self.trivia_room_instance.render()
        elif self.current_state == GameState.LOSE:
            mouse_pos = pygame.mouse.get_pos()
            self.lose_screen.draw(mouse_pos)
            
        if self.current_state in [GameState.MID_LEVEL, GameState.TRIVIA_ROOM]:
            self.hud.draw()
        pygame.display.flip()
        
    def trivia_room(self, selected_category):
        if self.trivia_room_instance is None:
            self.trivia_room_instance = TriviaGame(selected_category, self, self.screen)
        else:
            self.trivia_room_instance.category = selected_category
            self.trivia_room_instance.load_new_question()
        self.transition_state(GameState.TRIVIA_ROOM)

            
    def transition_state(self, new_state):
        self.current_state = new_state
        # Handle any setup needed for the new state
        if new_state == GameState.TRIVIA_ROOM:
            self.current_state = new_state
        elif new_state == GameState.MID_LEVEL:
            self.current_state = new_state
            # self.player.transition_to_state("mid_level")
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
