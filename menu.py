import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

font = pygame.font.Font(None, 36)

background_image = pygame.image.load('background.jpg').convert()

def draw_menu():
    screen.blit(background_image, [0, 0])

    draw_text("Trivia Trek", font, black, screen, 20, 20)
    draw_button("Start", 100, 200, 100, 50, white, blue, action=start_game)
    draw_button("Options", 100, 275, 100, 50, white, blue, action=options_game)
    draw_button("Quit", 100, 350, 100, 50, white, blue, action=quit_game)



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def options_game():
    print("Options selected...") 

def draw_button(text, x, y, width, height, text_color, button_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, button_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action() 
    else:
        pygame.draw.rect(screen, text_color, (x, y, width, height))

    draw_text(text, font, black, screen, x + 10, y + 10)

def start_game():
    print("Starting game...") 

def quit_game():
    pygame.quit()
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_menu()

    pygame.display.update()
