import pygame
from gamestate import GameState

class LoseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont('Arial', 74)
        self.font_small = pygame.font.SysFont('Arial', 40)
        self.try_again_rect = pygame.Rect(300, 400, 200, 50)
        self.quit_rect = pygame.Rect(300, 500, 200, 50)
        self.button_color = (255, 255, 255)
        self.button_hover_color = (200, 200, 200)
        self.skull_image = pygame.image.load('assets/img/skull.jpg')  
        desired_height = self.screen.get_height() * 0.4  
        aspect_ratio = self.skull_image.get_width() / self.skull_image.get_height()
        desired_width = int(desired_height * aspect_ratio)
        self.skull_image = pygame.transform.scale(self.skull_image, (desired_width, desired_height))
        
        # Vertical position of skull
        vertical_position = self.screen.get_height() // 2 - desired_height // 2 - -90  
        self.skull_rect = self.skull_image.get_rect(center=(self.screen.get_width() // 2, vertical_position))

        self.try_again_rect = pygame.Rect(300, 400, 200, 50)
        self.quit_rect = pygame.Rect(300, 500, 200, 50)

    def draw_text(self, text, font, color, center):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, rect, text, is_hovering):
        color = self.button_hover_color if is_hovering else self.button_color
        pygame.draw.rect(self.screen, color, rect)
        self.draw_text(text, self.font_small, (0, 0, 0), rect.center)


    def draw(self, mouse_pos):
        # Black screen background
        self.screen.fill((0, 0, 0)) 

        self.draw_text('You Lose!', self.font_big, (255, 0, 0), (self.screen.get_width() / 2, 100))

        # Centers skull
        self.screen.blit(self.skull_image, self.skull_rect)

        # Draw the buttons
        self.draw_button(self.try_again_rect, 'Try Again', self.try_again_rect.collidepoint(mouse_pos))
        self.draw_button(self.quit_rect, 'Quit', self.quit_rect.collidepoint(mouse_pos))

    def handle_event(self, event, transition_state_callback):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.try_again_rect.collidepoint(event.pos):
            # Transitions back to the main menu 
                transition_state_callback(GameState.MENU)
            elif self.quit_rect.collidepoint(event.pos):
                pygame.quit()
                exit()


