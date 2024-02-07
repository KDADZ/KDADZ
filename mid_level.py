import pygame
import sys

pygame.init()

portal_categories = ['a) history', 'b) video games', 'c) sports', 'd) food']

screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Trivia Trek')

# Load the background image and scale it to fit the screen
background_image = pygame.image.load('assets/img/background.png').convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load images for portals
portal_image = pygame.image.load('assets/img/portal1.png').convert_alpha()
portal_image = pygame.transform.scale(portal_image, (100, 100))

shop_portal_image = pygame.image.load('assets/img/portal2.png').convert_alpha()
shop_portal_image = pygame.transform.scale(shop_portal_image, (50, 50))

# Load stick figure image
stick_figure_image = pygame.image.load('assets/img/cropstickman.png').convert_alpha()
stick_figure_image = pygame.transform.scale(stick_figure_image, (50, 100))

# Ensure stick figure is scaled to fit above the portals
stick_figure_image = pygame.transform.scale(stick_figure_image, (50, 100))

# set initial stickman position
stickman_position = (screen_width - stick_figure_image.get_size()[0]) // 2

num_portals = len(portal_categories)  # 1 stick figure and 4 portals

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

stickman_speed = 1
fast_speed = 1
is_left_held = False
is_right_held = False

def handle_events():
    global stickman_position, is_left_held, is_right_held

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                is_left_held = True
            elif event.key == pygame.K_RIGHT:
                is_right_held = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                is_left_held = False
            elif event.key == pygame.K_RIGHT:
                is_right_held = False

def check_collisions(portal_x, portal_size, stickman_x, stickman_y, stickman_size):
    return (
        stickman_x < portal_x + portal_size and
        stickman_x + stickman_size > portal_x and
        stickman_y < screen_height - portal_size and
        stickman_y + stickman_size > (screen_height - portal_size) // 2
    )

def game_scene():
    global stickman_position
    while True:
        handle_events()

        # adjust speed of stickman
        current_speed = fast_speed if (is_left_held or is_right_held) else stickman_speed

        # update stickman position
        if is_left_held:
            stickman_position -= current_speed
        elif is_right_held:
            stickman_position += current_speed

        # Draw the background
        screen.blit(background_image, (0, 0))

        portal_size = portal_image.get_size()[0]
        portal_spacing = (screen_width - (num_portals * portal_size)) // (num_portals + 1)
        portal_start_x = portal_spacing
        # portal_y = (screen_height - portal_size) // 2

        # Draw portals and stick figure
        for i in range(num_portals):
            portal_x = portal_start_x + i * (portal_size + portal_spacing)
            portal_y = (screen_height - portal_size) // 2
            screen.blit(portal_image, (portal_x, portal_y))

            # draw stick figure above portals
            stick_figure_x = stickman_position
            stick_figure_y = portal_y - stick_figure_image.get_size()[1] - 10 # 10 pixels above the portal
            screen.blit(stick_figure_image, (stick_figure_x, stick_figure_y))

            if check_collisions(portal_x, portal_size, stick_figure_x, stick_figure_y, stick_figure_image.get_size()[1]):
                 print(f"Stickman collided with portal {portal_categories[i]}")

            # render and display portal categories
            category_font_size = 30
            category_font = pygame.font.Font(None, category_font_size)
            category_text = category_font.render(portal_categories[i], True, white)
            category_x = portal_x + (portal_size - category_text.get_size()[0]) // 2
            category_y = portal_y + portal_size + 5 # 5 pixels below the portal
            screen.blit(category_text, (category_x, category_y))

        # Draw shop portal
        shop_portal_x = screen_width - shop_portal_image.get_size()[0] - 20
        shop_portal_y = screen_height - shop_portal_image.get_size()[1] - 20
        screen.blit(shop_portal_image, (shop_portal_x, shop_portal_y))

        # Footer text
        level_difficulty = "Easy/Medium/Hard"
        footer_text = font.render(f"Level Difficulty: {level_difficulty}", True, white)
        screen.blit(footer_text, (10, screen_height - 40))

        pygame.display.flip()

game_scene()
