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

MAIN_MENU = 'main_menu'
OPTIONS_MENU = 'options_menu'
current_state = MAIN_MENU

def start_game():
    print("Starting game...")

def options_game():
    global current_state
    current_state = OPTIONS_MENU
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

def draw_main_menu(mouse_pos):
    screen.blit(background_image, (0, 0))
    draw_text("Trivia Trek", title_font, black, screen, screen_width // 2, 60)
    for text, button_data in buttons.items():
        draw_button(text, button_data["rect"], button_data["rect"].collidepoint(mouse_pos))

back_button_rect = pygame.Rect(50,50,100,50)
def draw_back_arrow(mouse_pos):
    global current_state
    if current_state == OPTIONS_MENU:
        pygame.draw.rect(screen, black, back_button_rect, 2)
        draw_text("Back", font, black, screen, back_button_rect.centerx, back_button_rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button_rect.collidepoint(mouse_pos):
                    current_state = MAIN_MENU

restart_button_rect = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)
quit_button_rect = pygame.Rect(screen_width // 2 - 100, 475, 200, 50)

def draw_options_menu(mouse_pos):
    screen.blit(background_image, (0, 0))
    draw_text("Options Menu", title_font, black, screen, screen_width // 2, 60)
    
    controls_text = [
        "Move Left: Arrow Left",
        "Move Right: Arrow Right",
        "Move Down: Arrow Down",
        "Move Up: Arrow Up"
    ]
    for i, text in enumerate(controls_text):
        draw_text(text, font, black, screen, screen_width // 2, 150 + i * 50)
    
   
    draw_button("Restart", restart_button_rect, restart_button_rect.collidepoint(mouse_pos))
    draw_button("Quit", quit_button_rect, quit_button_rect.collidepoint(mouse_pos))
    draw_back_arrow(mouse_pos)
    


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True  # Flag to indicate a click occurred this frame

    if current_state == MAIN_MENU:
        draw_main_menu(mouse_pos)
        if mouse_clicked:
            for button_text, button_data in buttons.items():
                if button_data["rect"].collidepoint(mouse_pos):
                    button_data["action"]()
    elif current_state == OPTIONS_MENU:
        draw_options_menu(mouse_pos)
        if mouse_clicked:
            if restart_button_rect.collidepoint(mouse_pos):
                current_state = MAIN_MENU
            elif quit_button_rect.collidepoint(mouse_pos):
                quit_game()
            elif back_button_rect.collidepoint(mouse_pos):
                current_state = MAIN_MENU 
        
    pygame.display.update()
