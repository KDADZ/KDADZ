
import pygame
import sys
import random

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
            self.background_image = pygame.image.load('assets/img/VictoryFinal.png').convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        except pygame.error as e:
            print(f"Failed to load the background image: {e}")
            sys.exit()

        try:
            self.rain_sock_image = pygame.image.load('assets/img/Victory_rain_sock.png').convert_alpha()
            self.rain_sock_image = pygame.transform.scale(self.rain_sock_image, (50, 50))
        except pygame.error as e:
            print(f"Failed to load the rain sock image: {e}")

        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.gold = (255, 215, 0)

        self.raining_socks = self.init_raining_socks(30)
        self.confetti = self.init_confetti(100)  # Number of confetti pieces

        # Attributes for the descending thank you message
        self.thank_you_message = "Thank You for Playing! Play Again Soon! Who On That Nag?"
        self.thank_you_pos_y = -50  # Start off-screen
        self.thank_you_target_y = 200  # Target y-coordinate

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

        score_text = self.font_small.render(f'Score: {getattr(self.game.player, "score", "Infinity And Beyond")}', True, self.gold)
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(score_text, score_rect)

        # Draw the thank you message
        if self.thank_you_pos_y < self.thank_you_target_y:
            self.thank_you_pos_y += 1
        thank_you_text = self.font_small.render(self.thank_you_message, True, self.gold)
        thank_you_rect = thank_you_text.get_rect(center=(self.screen.get_width() // 2, self.thank_you_pos_y))
        self.screen.blit(thank_you_text, thank_you_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("ESC pressed - Transitioning to another state not implemented.")

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game = type('Game', (object,), {"screen": screen, "player": type('Player', (object,), {"score": 12345})()})()
    victory_screen = VictoryScreen(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            victory_screen.handle_event(event)

        victory_screen.draw()
        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
