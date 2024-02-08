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

# Load the additional image (make sure to provide the correct path to the image)
additional_image_path = 'assets/img/Victory_sock.png'
additional_image = pygame.image.load(additional_image_path)

# Get the size of the image
image_width, image_height = additional_image.get_size()

# Calculate the new size to maintain aspect ratio and fit the screen height
new_height = screen_height
scale_factor = new_height / image_height
new_width = int(image_width * scale_factor)

# Resize the image
additional_image_resized = pygame.transform.scale(additional_image, (new_width, new_height))

# Calculate position to center the image
image_x = (screen_width - new_width) // 2
image_y = (screen_height - new_height) // 2

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

    # Display the resized additional image centered on the screen
    screen.blit(additional_image_resized, (image_x, image_y))

    # Congratulatory message
    text_victory = font_large.render('Congratulations!', True, white)
    screen.blit(text_victory, (200, 50))

    # Score and statistics
    text_score = font_small.render('Score: 12345', True, white)
    screen.blit(text_score, (200, 150))
    # Add more statistics as needed

    # TODO: Add more features (achievements, leaderboards, etc.) here

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

