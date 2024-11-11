import pygame
import sys

import functions
import settings

from button import Button

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((settings.screen_size, settings.screen_size))
pygame.display.set_caption("Highest Iceland Game")


# Font for buttons
text_font = pygame.font.SysFont("Times New Roman", 30)
# Font for buttons
accuracy_font = pygame.font.SysFont("Times New Roman", 20)

# Load the background image with alpha support
background_image = pygame.image.load("assets/bg_image.png").convert_alpha()
icon_image = pygame.image.load("assets/icon.png")  # Make sure the path is correct and the image is small

pygame.display.set_icon(icon_image)

# Scale the background image to fit the screen
background_image = pygame.transform.scale(background_image, (settings.screen_size, settings.screen_size))

# Set the opacity of the background image (e.g., 128 for 50% transparency)
background_image.set_alpha(128)

# Get the centered rect for the background image
background_rect = background_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Define a variable to track the popup state and message
show_popup = False
popup_message = ""

# Load the scroll popup image
popup_image = pygame.image.load("assets/bg_image.png").convert_alpha()  # Replace with your image file path
popup_image = pygame.transform.scale(popup_image, (600, 400))  # Resize if needed

def draw_popup(message):
    # Get the centered position for the popup
    popup_rect = popup_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Blit (draw) the image onto the main screen
    screen.blit(popup_image, popup_rect.topleft)


# Menu screen function
def menu_screen():
    # Create buttons
    play_button = Button(text="Play", pos=(screen.get_width() // 2, screen.get_height() // 2 - 100),
                         font=text_font, base_color="White", hovering_color="Green")
    quit_button = Button(text="Quit", pos=(screen.get_width() // 2, screen.get_height() // 2 + 50),
                         font=text_font, base_color="White", hovering_color="Red")
    stats_button = Button(text="Stats", pos=(screen.get_width() // 2, screen.get_height() // 2 - 25),
                         font=text_font, base_color="White", hovering_color="Blue")

    while True:
        # Blit the background image with transparency
        screen.blit(background_image, background_rect.topleft)

        menu_mouse_pos = pygame.mouse.get_pos()

        # Update button colors based on mouse position
        play_button.change_color(menu_mouse_pos)
        quit_button.change_color(menu_mouse_pos)
        stats_button.change_color(menu_mouse_pos)

        # Draw buttons
        play_button.update(screen)
        quit_button.update(screen)
        stats_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    # Start the game
                    play_screen()
                elif stats_button.check_for_input(menu_mouse_pos):
                    # Stats in the game
                    stats_screen()
                elif quit_button.check_for_input(menu_mouse_pos):
                    # Quit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Play screen function
# Play screen function
def play_screen():
    global show_popup, popup_message  # Declare these as global to modify them

    lives = 3  # Number of lives

    # Load the heart image
    heart_image = pygame.image.load("assets/heart.png")
    heart_image = pygame.transform.scale(heart_image, (50, 30))  # Resize if necessary

    # Island data
    matrix = functions.get_game_data()

    # Sand image
    sand = pygame.image.load("assets/sand.jpg")
    sand = pygame.transform.scale(sand, (settings.cell_size, settings.cell_size))

    # Load the background image
    background = pygame.image.load("assets/sea.jpg").convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    background_width = background.get_width()

    x_offset = 0  # Initial x position of the background
    scroll_speed = 0.01  # Adjust the speed of background scrolling

    # Run the main game loop here
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the menu when Esc is pressed
                    running = False
            # Detect mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Close the popup if it's visible
                    if show_popup:
                        show_popup = False  # Close the popup when clicked
                    else:
                        # Calculate the row and column in the matrix
                        col = mouse_x // settings.cell_size
                        row = mouse_y // settings.cell_size

                        # Check if the click is within the grid boundaries
                        if 0 <= row < settings.grid_size and 0 <= col < settings.grid_size:
                            print(f"Clicked on row: {row}, col: {col}")

                            # Check if there is an image at this position
                            if matrix[row][col] > 0:
                                print(f"Image found at row: {row}, col: {col}, value: {matrix[row][col]}")
                                show_popup = True  # Show the popup
                                popup_message = f"Image found at row: {row}, col: {col}, value: {matrix[row][col]}"

        # Update the x_offset for scrolling
        x_offset -= scroll_speed
        if x_offset <= -background_width:
            x_offset = 0  # Reset offset to create continuous scrolling

        # Draw the background twice for seamless scrolling
        screen.blit(background, (x_offset, 0))
        screen.blit(background, (x_offset + background_width, 0))

        # Go through the matrix
        for row in range(settings.grid_size):
            for col in range(settings.grid_size):
                if matrix[row][col] > 0:
                    # Calculate the position of each cell
                    x = col * settings.cell_size
                    y = row * settings.cell_size

                    # Draw the image at this position
                    screen.blit(sand, (x, y))

        # Draw lives (hearts) in the top right corner
        for i in range(lives):
            screen.blit(heart_image, (screen.get_width() - (i + 1) * 50, 10))

        accuracy = 85  # Example accuracy value; replace with your actual variable

        # Insert the variable in the string using an f-string
        draw_text(f"Accuracy: {accuracy}%", accuracy_font, (0, 0, 0), 10, 10)

        # Draw the popup if it's active
        if show_popup:
            draw_popup(popup_message)

        pygame.display.update()


def stats_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to the menu when Esc is pressed
                    running = False

        screen.fill((0, 100, 100))  # Example background color for the play screen
        draw_text("Playing the Game! Press Esc to go back.", text_font, (255, 255, 255), 50, 50)
        pygame.display.update()

# Function to render text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Start with the menu screen
menu_screen()
