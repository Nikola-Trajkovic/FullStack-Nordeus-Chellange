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
# Font for accuracy and message text
accuracy_font = pygame.font.SysFont("Times New Roman", 20)
button_font = pygame.font.SysFont("Times New Roman", 24)

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
button_type = ""

# Load the popup background image
popup_background = pygame.image.load("assets/popup.png").convert_alpha()
popup_background = pygame.transform.scale(popup_background, (300, 200))  # Initial size; will be resized dynamically

# Colors for buttons
button_color = (70, 130, 180)
button_hover_color = (100, 180, 240)
button_text_color = (0, 0, 0)


def draw_popup(message, popup_button_type):
    # Render the message text to calculate its width and adjust the popup size
    message_surface = accuracy_font.render(message, True, (0, 0, 0))
    message_width, message_height = message_surface.get_size()

    # Set popup width and height based on message dimensions, and make it fit well with the scroll background
    popup_width = max(message_width + 100, 650)  # Add padding, with a minimum width
    popup_height = 500  # Fixed height for the scroll popup background

    # Resize the popup background (scroll) to fit the calculated width and height
    popup_image = pygame.transform.scale(popup_background, (popup_width, popup_height))
    popup_rect = popup_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Draw the popup background
    screen.blit(popup_image, popup_rect.topleft)

    # Center the message text horizontally, position it towards the top half
    message_rect = message_surface.get_rect(center=(popup_rect.centerx, popup_height // 2))
    screen.blit(message_surface, message_rect.topleft)

    # Render a single button based on popup_button_type
    button_width, button_height = 150, 30  # Smaller button
    button_rect = pygame.Rect(0, 0, button_width, button_height)
    button_rect.center = (popup_rect.centerx, popup_height // 2 + 45)  # Add padding from bottom of scroll

    # Draw button with specified label
    pygame.draw.rect(screen, button_color, button_rect)

    # Check the button type and render the appropriate text
    if popup_button_type == "Retry":
        button_text_surface = button_font.render("Retry", True, button_text_color)
    elif popup_button_type == "Next Level":
        button_text_surface = button_font.render("Next Level", True, button_text_color)
    else:
        button_text_surface = None  # No button if an unrecognized button_type is passed

    # Draw the button text if valid and center it within the button
    if button_text_surface:
        button_text_rect = button_text_surface.get_rect(center=button_rect.center)
        screen.blit(button_text_surface, button_text_rect.topleft)

    return button_rect if button_text_surface else None  # Return button rect for click detection, or None



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


total_lives = 3
lives = 3

success_level = 0
tries = 0

# Island data
matrix = functions.get_game_data()
goal = functions.find_max_island_height(matrix)

# Play screen function
def play_screen():
    global show_popup, popup_message, button_type, lives, total_lives, tries, success_level, matrix, goal  # Declare globals to modify popup state

    # Load the heart image
    heart_image = pygame.image.load("assets/heart.png")
    heart_image = pygame.transform.scale(heart_image, (50, 30))  # Resize if necessary

    # Load the x image
    x_image = pygame.image.load("assets/x.png")
    x_image = pygame.transform.scale(x_image, (40, 30))  # Resize if necessary


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
                    tries += 1

                    # Close the popup if it's visible
                    if show_popup:
                        button_rect = draw_popup(popup_message, button_type)
                        if button_rect and button_rect.collidepoint(mouse_x, mouse_y):
                            if button_type == "Retry":
                                print("Retry button clicked")

                                if lives == 0:
                                    lives = 3
                                    matrix = functions.get_game_data()
                                    goal = functions.find_max_island_height(matrix)

                                # Add retry logic here
                            elif button_type == "Next Level":

                                lives = 3
                                matrix = functions.get_game_data()
                                goal = functions.find_max_island_height(matrix)

                                print("Next Level button clicked")
                                # Add next level logic here
                            show_popup = False  # Close popup after button click
                    else:
                        # Calculate the row and column in the matrix
                        col = mouse_x // settings.cell_size
                        row = mouse_y // settings.cell_size

                        # Check if the click is within the grid boundaries
                        if 0 <= row < settings.grid_size and 0 <= col < settings.grid_size:

                            # Check if there is an image at this position
                            if matrix[row][col] > 0:
                                visited = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
                                height_sum = [0]
                                iteration = [0]

                                # Perform DFS on this cell to explore the entire island
                                functions.dfs_island(matrix, row, col, visited, height_sum, iteration)

                                # Calculate the height metric (sum/iterations)
                                current_height = round(height_sum[0] / iteration[0] if iteration[0] > 0 else 0, 2)
                                print(current_height)
                                print(goal)
                                if current_height == goal:
                                    show_popup = True  # Show the popup
                                    popup_message = f"Image found at row: {row}, col: {col}, value: {matrix[row][col]}"
                                    button_type = "Next Level"  # or "Retry" based on your logic
                                else:
                                    print(f"Clicked on row: {row}, col: {col}")
                                    lives -= 1
                                    button_type = "Retry"
                                    show_popup = True  # Show the popup

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



        # Draw lives (hearts or "X") in the top right corner
        for i in range(total_lives):
            if i < lives:
                # Draw a heart if the player still has this life
                screen.blit(heart_image, (screen.get_width() - (i + 1) * 50, 10))
            else:
                # Draw an "X" if this life has been lost
                screen.blit(x_image, (screen.get_width() - (i + 1) * 50, 10))

        if tries > 0:
            accuracy = round((success_level/tries) * 100, 2)
            draw_text(f"Accuracy: {accuracy}%", accuracy_font, (0, 0, 0), 10, 10)

        # Draw the popup if it's active and capture the button rect for click detection
        button_rect = None
        if show_popup:
            draw_popup(popup_message, button_type)

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
