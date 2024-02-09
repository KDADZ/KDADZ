
import pygame
import sys
import random
from gamestate import GameState

class Particle:
    def __init__(self, x, y, radius, color, lifetime, x_vel, y_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):
        self.x_vel *= 0.99  # Air resistance
        self.y_vel += 0.05  # Gravity
        self.x += self.x_vel
        self.y += self.y_vel
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class VictoryScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        try:

            self.background_image = pygame.image.load('assets/img/Victory_sock.png').convert_alpha()
            self.bg_image_rect = self.background_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            # Load and potentially resize the rain sock image
            self.rain_sock_image = pygame.image.load('assets/img/Victory_rain_sock.png').convert_alpha()
            self.rain_sock_image = pygame.transform.scale(self.rain_sock_image, (50, 50))  # Adjust size as needed

        except pygame.error as e:
            print(f"Failed to load the background image: {e}")
            sys.exit()

        self.font_large = pygame.font.Font('protest.ttf', 74)
        self.font_small = pygame.font.Font('protest.ttf', 50)
        self.gold = (255, 215, 0)
        
        # self.buttons = {
        #     'Menu': {'rect': pygame.Rect(150, 300, 200, 50), 'action': self.go_to_menu, 'label': 'Menu'},
        #     'Quit': {'rect': pygame.Rect(450, 300, 200, 50), 'action': self.quit_game, 'label': 'Quit'},
        #     'Special': {'rect': pygame.Rect(300, 400, 200, 50), 'action': self.special_action, 'label': 'Special'}  # Placeholder for special action
        # }
        
        self.buttons = {
            'Menu': {'rect': pygame.Rect(150, 150, 200, 50), 'action': self.go_to_menu, 'label': 'Menu'},  # y changed from 300 to 250
            'Quit': {'rect': pygame.Rect(450, 150, 200, 50), 'action': self.quit_game, 'label': 'Quit'},  # y changed from 300 to 250
            'Special': {'rect': pygame.Rect(300, 225, 200, 50), 'action': self.special_action, 'label': 'Credits?'}  # y changed from 400 to 350
        }
        
        # Initialize raining socks
        self.raining_socks = self.init_raining_socks(30)  # Adjust the number of socks as needed
        
    def go_to_menu(self):
        self.game.transition_state(GameState.MENU)
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def special_action(self):
        self.game.transition_state(GameState.CREDITS_SCENE)


    def init_raining_socks(self, num_socks):
        socks = []
        for _ in range(num_socks):
            x_pos = random.randint(0, self.screen.get_width())
            y_pos = random.randint(-self.screen.get_height(), 0)
            speed = random.randint(2, 6)
            socks.append([x_pos, y_pos, speed])
        return socks

    def update_raining_socks(self):
        for sock in self.raining_socks:
            sock[1] += sock[2]
            if sock[1] > self.screen.get_height():
                sock[0] = random.randint(0, self.screen.get_width())
                sock[1] = random.randint(-100, 0)

    def init_confetti(self, num_pieces):
        confetti = []
        for _ in range(num_pieces):
            x_pos = random.randint(0, self.screen.get_width())
            y_pos = random.randint(-self.screen.get_height(), 0)
            speed = random.randint(1, 4)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            confetti.append([x_pos, y_pos, speed, color])
        return confetti

    def update_confetti(self):
        for piece in self.confetti:
            piece[1] += piece[2]
            if piece[1] > self.screen.get_height():
                piece[0] = random.randint(0, self.screen.get_width())
                piece[1] = random.randint(-100, 0)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.update_raining_socks()
        for sock in self.raining_socks:
            self.screen.blit(self.rain_sock_image, (sock[0], sock[1]))

        self.update_confetti()
        for piece in self.confetti:
            pygame.draw.rect(self.screen, piece[3], pygame.Rect(piece[0], piece[1], 5, 5))

        text_victory = self.font_large.render('Congratulations!', True, self.gold)
        text_rect = text_victory.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text_victory, text_rect)

        score_text = f'Score: {self.game.player.money}'
        text_score = self.font_small.render(score_text, True, self.gold)
        score_rect = text_score.get_rect(center=(self.screen.get_width() // 2, 125))
        self.screen.blit(text_score, score_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        for button_key, button_info in self.buttons.items():
            fill_color = (0, 0, 0)  # Black color for button fill
            border_color = (255, 255, 255) if button_info['rect'].collidepoint(mouse_pos) else (200, 200, 200)  # White when hovered, otherwise light gray
            pygame.draw.rect(self.screen, fill_color, button_info['rect'])
            text_surface = self.font_small.render(button_info['label'], True, border_color)  # Use border_color for text to match the border
            text_rect = text_surface.get_rect(center=button_info['rect'].center)
            self.screen.blit(text_surface, text_rect)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pygame.mouse.get_pos()
            for button_key, button_info in self.buttons.items():
                if button_info['rect'].collidepoint(mouse_pos):
                    button_info['action']()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_to_menu()

