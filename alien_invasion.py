import sys

import pygame

def run_game():
    #initialize game and create a screen object.

    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Alien Invasion")

    # Set the background color
    bg_color = (0, 0, 230)

    # Start the main loop for the game.
    count = 1
    while True:

        # Watch for keboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

        # Redraw the screen during each pass thorugh the loop.
        screen.fill(bg_color)

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        
run_game()
