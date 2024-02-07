import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Victory Screen')

# Load background image
background_image = pygame.image.load('assets/img/victory_screen.png')

# Define colors
white = (255, 255, 255)

# Set up fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display the background
    screen.blit(background_image, (0, 0))

    # Congratulatory message
    text_victory = font_large.render('Congratulations!', True, white)
    screen.blit(text_victory, (200, 50))

    # Score and statistics
    text_score = font_small.render('Score: 12345', True, white)
    screen.blit(text_score, (200, 150))
    # Add more statistics as needed

    # TODO: Add more features (characters celebration, achievements, etc.) here

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
