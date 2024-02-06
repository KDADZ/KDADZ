import pygame
import sys
from gamestate import GameState

class Menu:
    def __init__(self, game):
        self.game = game
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.screen = game.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.current_state = 'main_menu'
        
        self.background_image = pygame.image.load('background.jpg').convert_alpha()
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 80)
        
        self.buttons = {
            "Start": {"rect": pygame.Rect(self.screen_width // 2 - 100, 200, 200, 50), "action": self.start_game},
            "Options": {"rect": pygame.Rect(self.screen_width // 2 - 100, 275, 200, 50), "action": self.options_game},
            "Quit": {"rect": pygame.Rect(self.screen_width // 2 - 100, 350, 200, 50), "action": self.quit_game}
        }
        
        self.back_button_rect = pygame.Rect(50, 50, 100, 50)
        self.restart_button_rect = pygame.Rect(self.screen_width // 2 - 100, 400, 200, 50)
        self.quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, 475, 200, 50)

    def start_game(self):
        self.game.transition_state(GameState.MID_LEVEL)

    def options_game(self):
        self.current_state = 'options_menu'

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True  # Mouse was clicked this frame

        if self.current_state == 'main_menu':
            if mouse_clicked:
                for _, button_data in self.buttons.items():
                    if button_data["rect"].collidepoint(mouse_pos):
                        button_data["action"]()
        elif self.current_state == 'options_menu':
            if mouse_clicked:
                if self.restart_button_rect.collidepoint(mouse_pos):
                    # Handle restart button click
                    self.current_state = 'main_menu'
                elif self.quit_button_rect.collidepoint(mouse_pos):
                    # Handle quit button click
                    self.quit_game()
                elif self.back_button_rect.collidepoint(mouse_pos):
                    # Handle back button click
                    self.current_state = 'main_menu'

    def draw(self, mouse_pos):
        self.screen.blit(self.background_image, (0, 0))
        if self.current_state == 'main_menu':
            self.draw_main_menu(mouse_pos)
        elif self.current_state == 'options_menu':
            self.draw_options_menu(mouse_pos)
        pygame.display.update()

    def draw_main_menu(self, mouse_pos):
        self.draw_text("Trivia Trek", self.title_font, self.black, self.screen_width // 2, 60)
        for text, button_data in self.buttons.items():
            self.draw_button(text, button_data["rect"], button_data["rect"].collidepoint(mouse_pos))

    def draw_options_menu(self, mouse_pos):
        self.draw_text("Options Menu", self.title_font, self.black, self.screen_width // 2, 60)
        # Other options we think of
        self.draw_button("Restart", self.restart_button_rect, self.restart_button_rect.collidepoint(mouse_pos))
        self.draw_button("Quit", self.quit_button_rect, self.quit_button_rect.collidepoint(mouse_pos))
        self.draw_back_arrow(mouse_pos)

    def draw_button(self, text, rect, active):
        text_color = self.blue if active else self.black
        pygame.draw.rect(self.screen, text_color, rect, 2)
        self.draw_text(text, self.font, text_color, rect.centerx, rect.centery)

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_back_arrow(self, mouse_pos):
        pygame.draw.rect(self.screen, self.black, self.back_button_rect, 2)
        self.draw_text("Back", self.font, self.black, self.back_button_rect.centerx, self.back_button_rect.centery)
