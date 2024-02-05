import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255) 

background_image = pygame.image.load('background.jpg').convert_alpha()

font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 80) 

def start_game():
    print("Starting game...")

def options_game():
    print("Options menu...")

def quit_game():
    pygame.quit()
    sys.exit()

buttons = {
    "Start": {"rect": pygame.Rect(screen_width // 2 - 100, 200, 200, 50), "action": start_game},
    "Options": {"rect": pygame.Rect(screen_width // 2 - 100, 275, 200, 50), "action": options_game},
    "Quit": {"rect": pygame.Rect(screen_width // 2 - 100, 350, 200, 50), "action": quit_game}
}

def draw_button(text, rect, active):
    text_color = blue if active else black 
    draw_text(text, font, text_color, screen, rect.centerx, rect.centery)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_menu(mouse_pos):
    screen.blit(background_image, (0, 0))

    draw_text("Trivia Trek", title_font, black, screen, screen_width // 2, 60)

    for text, button_data in buttons.items():
        draw_button(text, button_data["rect"], button_data["rect"].collidepoint(mouse_pos))

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button_text, button_data in buttons.items():
                    if button_data["rect"].collidepoint(mouse_pos):
                        button_data["action"]()

    draw_menu(mouse_pos)

    pygame.display.update()
