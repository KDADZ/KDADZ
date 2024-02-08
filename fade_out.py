import pygame

def fade_out(screen, final_alpha=255, color=(0, 0, 0), speed=5):
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill(color)
    for alpha in range(0, final_alpha + 1, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)