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
        pygame.mixer.music.load('assets/Music/catch_the_starlight_8bit.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        self.background_image = pygame.image.load('assets/img/background.jpg').convert_alpha()
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
        
        # Attributes for the volume slider
        # self.volume_slider_rect = pygame.Rect(self.screen_width // 2 - 100, 350, 200, 20)
        # self.volume_handle_rect = pygame.Rect(self.volume_slider_rect.centerx - 10, self.volume_slider_rect.y - 5, 20, 30)
        self.volume_slider_rect = pygame.Rect(self.screen_width // 2 - 150, 450, 300, 30)
        self.volume_handle_rect = pygame.Rect(self.volume_slider_rect.centerx - 15, self.volume_slider_rect.y - 10, 30, 50)
        self.volume = pygame.mixer.music.get_volume()
        self.dragging_volume_handle = False
        self.update_volume_handle_pos()

    def update_volume_handle_pos(self):
        self.volume_handle_rect.centerx = self.volume_slider_rect.x + self.volume * self.volume_slider_rect.width

    def start_game(self):
        self.game.transition_state(GameState.MID_LEVEL)

    def options_game(self):
        self.current_state = 'options_menu'

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.current_state == 'options_menu' and self.volume_handle_rect.collidepoint(mouse_pos):
                    self.dragging_volume_handle = True
                elif self.back_button_rect.collidepoint(mouse_pos):
                    self.current_state = 'main_menu'
                elif self.quit_button_rect.collidepoint(mouse_pos):
                    self.quit_game()
                else:
                    for _, button_data in self.buttons.items():
                        if button_data["rect"].collidepoint(mouse_pos):
                            button_data["action"]()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_volume_handle = False

            elif event.type == pygame.MOUSEMOTION and self.dragging_volume_handle:
                new_x = min(max(event.pos[0], self.volume_slider_rect.left), self.volume_slider_rect.right)
                self.volume_handle_rect.centerx = new_x
                self.volume = (new_x - self.volume_slider_rect.x) / self.volume_slider_rect.width
                pygame.mixer.music.set_volume(self.volume)

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
        # Draw volume slider and label
        pygame.draw.rect(self.screen, self.white, self.volume_slider_rect)
        pygame.draw.rect(self.screen, self.blue if self.volume_handle_rect.collidepoint(mouse_pos) else self.black, self.volume_handle_rect)
        self.draw_volume_label()

        # Draw other options buttons
        self.draw_button("Back", self.back_button_rect, self.back_button_rect.collidepoint(mouse_pos))

    def draw_button(self, text, rect, is_hovering):
        color = self.blue if is_hovering else self.black
        pygame.draw.rect(self.screen, color, rect)  # Solid fill
        self.draw_text(text, self.font, self.white, rect.centerx, rect.centery)

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_volume_label(self):
        volume_label_text = "Volume"
        volume_label_color = self.black
        volume_label_font = pygame.font.Font(None, 45)  # Increased font size
        volume_label_surface = volume_label_font.render(volume_label_text, True, volume_label_color)
        volume_label_x = self.volume_slider_rect.x - volume_label_surface.get_width() - 20  # Adjust position if needed
        volume_label_y = self.volume_slider_rect.y - volume_label_surface.get_height() // 100  # Adjust for new font size
        self.screen.blit(volume_label_surface, (volume_label_x, volume_label_y))
