# victory_screen.py
import pygame

class VictoryScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.background_image = pygame.image.load('assets/img/victory_screen.png').convert_alpha()
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        # Load other resources as needed

    def draw(self):
        # Blit the background image
        self.screen.blit(self.background_image, (0, 0))

        # Congratulatory message
        text_victory = self.font_large.render('Congratulations!', True, (255, 255, 255))
        text_rect = text_victory.get_rect(center=(self.screen.get_width()//2, 50))
        self.screen.blit(text_victory, text_rect)

        # Score and statistics (Example)
        text_score = self.font_small.render(f'Score: {self.game.player.points}', True, (255, 255, 255))
        score_rect = text_score.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(text_score, score_rect)
        # Add more statistics as needed

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Example: Press ESC to return to menu
                self.game.transition_state(GameState.MENU)
        # Add more event handling if needed
