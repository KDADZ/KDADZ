import pygame

class HUD:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.hud_surface = pygame.Surface((self.game.screen.get_width(), 60))
        self.font = pygame.font.Font("protest.ttf", 32)
        self.red_potion_image = pygame.image.load('assets/img/red_POT.png').convert_alpha()
        self.red_potion_image = pygame.transform.scale(self.red_potion_image, (50, 60))
        self.heart_frames = [pygame.image.load(f'resized_frames/heart_frame_{i}.png').convert_alpha() for i in range(45)]
        self.empty_heart_image = pygame.image.load('resized_frames/empty_heart.png').convert_alpha()
        self.e_key_box = pygame.Rect(0, 0, 40, 40)
        
    def draw(self):
        self.hud_surface.fill((0, 0, 0))
        self.draw_hearts()
        base_y = self.screen.get_height() - 37
        level_x = 200

        points_text = f"Points: {self.game.player.points}"
        self.draw_text(points_text, level_x, base_y)

        level_text = f"Level: {self.game.current_level}"
        self.draw_text(level_text, 10, base_y)
        
        potion_y = self.screen.get_height() - 60
        potion_count = self.game.player.inventory.items.get('Health Potion', 0)
        potion_x = self.game.screen.get_width() - 90  # Adjust X to move the potion icon left or right
        self.screen.blit(self.red_potion_image, (potion_x, potion_y))
        self.draw_text(f"x{potion_count}", potion_x + 45, potion_y - 8)
        
        e_key_x = potion_x - 40
        e_key_y = potion_y + 10
        e_key_text = "E"
        self.e_key_box = pygame.Rect(e_key_x - 10, e_key_y - 10, 40, 40)  # Adjust dimensions as needed

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering_e = self.e_key_box.collidepoint(mouse_pos)

        box_color = (100, 100, 255) if self.is_hovering_e else (255, 255, 255)
        pygame.draw.rect(self.screen, box_color, self.e_key_box, 0)  # Filled box
        pygame.draw.rect(self.screen, (255, 255, 255), self.e_key_box, 2)  # Optional border

        e_key_surface = self.font.render(e_key_text, True, (0, 0, 0))  # Black text for visibility
        e_key_rect = e_key_surface.get_rect(center=(self.e_key_box.centerx, self.e_key_box.centery))
        self.screen.blit(e_key_surface, e_key_rect.topleft)
        
        
        
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

# import pygame

# class HUD:
#     def __init__(self, game):
#         self.game = game
#         self.screen = game.screen
#         # Create a HUD surface with transparency
#         self.hud_surface = pygame.Surface((self.game.screen.get_width(), 60), pygame.SRCALPHA)
#         self.font = pygame.font.Font("protest.ttf", 32)
#         self.heart_frames = [pygame.image.load(f'resized_frames/heart_frame_{i}.png').convert_alpha() for i in range(45)]
#         self.empty_heart_image = pygame.image.load('resized_frames/empty_heart.png').convert_alpha()

#     def draw(self):
#         # Fill HUD surface with transparency (or a solid color if preferred)
#         self.hud_surface.fill((0, 0, 0, 0))  # RGBA for transparent fill
#         self.draw_hearts()
#         base_y = 10  # Adjust if needed, used for positioning text on the HUD surface

#         # Draw additional HUD elements like money and level
#         money_text = f"Money: {self.game.player.money}"
#         self.draw_text(money_text, 200, base_y)  # Adjust position as needed

#         level_text = f"Level: {self.game.current_level}"
#         self.draw_text(level_text, 10, base_y)

#         # Finally, blit the entire HUD surface onto the main screen
#         self.screen.blit(self.hud_surface, (0, self.game.screen.get_height() - 60))

#     def draw_hearts(self):
#         max_health = self.game.player.max_hp
#         current_health = self.game.player.hp
        
#         # Draw full and empty hearts on the HUD surface
#         for i in range(max_health):
#             heart_x = 10 + (i * 40)  # Space the hearts out
#             if i < current_health:
#                 self.hud_surface.blit(self.heart_frames[0], (heart_x, 10))  # Assuming frame 0 is the full heart
#             else:
#                 self.hud_surface.blit(self.empty_heart_image, (heart_x, 10))
        
#         # Optionally animate the active heart if desired
#         if current_health > 0:
#             self.animate_active_heart(current_health - 1)

#     def animate_active_heart(self, heart_index):
#         current_time = pygame.time.get_ticks()
#         frame_duration = 1000 // len(self.heart_frames)  # Adjust the speed
#         frame_index = (current_time // frame_duration) % len(self.heart_frames)
#         heart_x = 10 + (heart_index * 40)  # Match the X position with draw_hearts
#         # Animate on the HUD surface
#         self.hud_surface.blit(self.heart_frames[frame_index], (heart_x, 10))

#     def draw_text(self, text, x, y):
#         text_surface = self.font.render(text, True, (255, 255, 255))
#         # Draw text on the HUD surface
#         self.hud_surface.blit(text_surface, (x, y))
