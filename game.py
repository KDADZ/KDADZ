import pygame
from player import Player
from items import red_potion
from trivia_room import TriviaGame
from gamestate import GameState
from menu import Menu
from lose_screen import LoseScreen
from hud import HUD
from midplayer import MidLevel
from item_shop import ItemShop
from fade_out import fade_out
from victory_screen import VictoryScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        pygame.display.set_caption("Trivia Trek")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.menu = Menu(self)
        self.hud = HUD(self)
        self.mid_level = MidLevel(self)

        self.player = Player(5, 100)
        self.player.add_item(red_potion, 1)
        self.trivia_room_instance = None
        self.current_level = 1

        self.lose_screen = LoseScreen(self.screen)
    
        self.item_shop = ItemShop(self.screen, self.player, self)

        self.victory_screen = VictoryScreen(self)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left click
                if self.hud.e_key_box.collidepoint(mouse_pos) and self.current_state in [GameState.MID_LEVEL, GameState.TRIVIA_ROOM]:
                    self.player.use_health_potion()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:  # Press 'L' key to simulate losing
                    self.transition_state(GameState.LOSE)
                elif event.key == pygame.K_s and self.current_state == GameState.MID_LEVEL:  # Ensure we're in MID_LEVEL
                    self.transition_state(GameState.SHOP)
                elif event.key == pygame.K_m:  # Press 'M' key to return to mid-level screen
                    self.transition_state(GameState.MID_LEVEL)
                elif event.key == pygame.K_i:  # 'i' key to open the inventory
                    self.open_inventory()
                elif event.key == pygame.K_e:
                    self.player.use_health_potion()
                elif event.key == pygame.K_v:  # 'v' key to open the victory screen
                    self.open_victory_screen()  # Corrected to call the right method
                elif event.key == pygame.K_p: # 'p' to add points for testing
                    self.player.add_points(500)

            if self.current_state == GameState.MENU:
                self.menu.handle_events(events)
            elif self.current_state == GameState.MID_LEVEL:
                self.mid_level.handle_events(events)
            elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
                self.trivia_room_instance.handle_events(events)
            elif self.current_state == GameState.LOSE:
                self.lose_screen.handle_event(event, self.transition_state)
            elif self.current_state == GameState.SHOP:
                self.item_shop.handle_event(event, self.transition_state)
            elif self.current_state == GameState.VICTORY:
                self.victory_screen.handle_event(event)

    def update(self):
        if self.player.hp <= 0:
            self.transition_state(GameState.LOSE)
        elif self.current_state == GameState.MID_LEVEL:
            self.mid_level.update()
        elif self.current_state == GameState.TRIVIA_ROOM and self.trivia_room_instance:
            self.trivia_room_instance.update()
        elif self.current_state == GameState.LOSE:
            pass  
        elif self.current_state == GameState.SHOP:
            pass  

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
        elif self.current_state == GameState.SHOP:
            self.item_shop.draw() 
        elif self.current_state == GameState.INVENTORY:
            self.player.inventory.draw(self.screen)
        elif self.current_state == GameState.VICTORY:
            self.victory_screen.draw()

        if self.current_state in [GameState.MID_LEVEL, GameState.TRIVIA_ROOM]:
            self.hud.draw()
        
    def trivia_room(self, selected_category):
        if self.trivia_room_instance is None:
            self.trivia_room_instance = TriviaGame(selected_category, self, self.screen)
        else:
            self.trivia_room_instance.category = selected_category
            self.trivia_room_instance.load_new_question()
        self.transition_state(GameState.TRIVIA_ROOM)

    def open_inventory(self):
        if self.current_state != GameState.INVENTORY:
            self.previous_state = self.current_state  
            self.current_state = GameState.INVENTORY  
        else:
            self.current_state = self.previous_state
            
    def reset_game(self):
            self.player.hp = self.player.max_hp
            self.player.money = 100  # Reset to initial money, adjust as needed
            self.player.points = 0
            # self.player.inventory.clear()
            self.player.add_item(red_potion, 1)  # Give initial items back, adjust as needed
            self.current_level = 1
            self.trivia_room_instance = None
            
    def open_victory_screen(self):
        self.transition_state(GameState.VICTORY)

    def transition_state(self, new_state):
        fade_out(self.screen)
        
        if self.current_state == GameState.LOSE and new_state == GameState.MENU:
            self.reset_game()
            
        self.current_state = new_state
        
        if new_state == GameState.TRIVIA_ROOM:
            self.current_state = new_state
        # Load and play background music for the trivia room
            pygame.mixer.music.load('assets\Music\\trivia_room.mp3')
            pygame.mixer.music.play(-1)  # Loop the music
        elif new_state == GameState.MID_LEVEL:
            # Load and play background music for the mid-level
            pygame.mixer.music.load('assets\Music\Mid_Level.mp3')
            pygame.mixer.music.play(-1)  # Loop the music

        elif new_state == GameState.MENU:
            # Load and play background music for the menu
            self.reset_game()
            pygame.mixer.music.load('assets\Music\main_menu.mp3')
            pygame.mixer.music.play(-1)  # Loop the music

        elif new_state == GameState.LOSE:
            # Load and play background music for the lose screen
            self.reset_game()
            pygame.mixer.music.load('assets\Music\lose_screen.mp3')

        elif new_state == GameState.VICTORY:
            # pygame.mixer.music.load('assets\Music\victory_screen.mp3')
            # pygame.mixer.music.play(-1)
            pass
            
        elif new_state == GameState.SHOPKEEPER:
            pygame.mixer.music.load('assets\Music\shop_menu.mp3')
            pygame.mixer.music.play(-1)
        elif new_state == GameState.SHOP:
            pass

    def allow_redo(self):
        pass
    
    def skip_round(self):
        pass
    
    def trivia_room_logic():
        pass
