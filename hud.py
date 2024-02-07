import pygame

class HUD:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font("protest.ttf", 32)
        self.heart_frames = [pygame.image.load(f'resized_frames/heart_frame_{i}.png').convert_alpha() for i in range(45)]
        self.empty_heart_image = pygame.image.load('resized_frames/empty_heart.png').convert_alpha()
        
    def draw(self):
        self.draw_hearts()
        base_y = self.screen.get_height() - 37
        level_x = 200

        money_text = f"Money: {self.game.player.money}"
        self.draw_text(money_text, level_x, base_y)

        level_text = f"Level: {self.game.current_level}"
        self.draw_text(level_text, 10, base_y)


    def draw_hearts(self):
        max_health = self.game.player.max_hp
        current_health = self.game.player.hp
        
        for i in range(current_health):
            heart_x = 10 + (i * 40)  # Space the hearts out
            self.screen.blit(self.heart_frames[0], (heart_x, 10))
        
        for i in range(current_health, max_health):
            heart_x = 10 + (i * 40)
            self.screen.blit(self.empty_heart_image, (heart_x, 10))
        
        # Animate the active heart
        if current_health > 0:
            self.animate_active_heart(current_health - 1)

    def animate_active_heart(self, heart_index):
        current_time = pygame.time.get_ticks()
        frame_duration = 1000 // len(self.heart_frames)  # Adjust the speed
        frame_index = (current_time // frame_duration) % len(self.heart_frames)
        heart_x = 10 + (heart_index * 40)  # Match the X position with draw_hearts
        self.screen.blit(self.heart_frames[frame_index], (heart_x, 10))

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))
