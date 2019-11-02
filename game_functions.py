import sys
import pygame

def check_events(ship):
    """ Respond to keypresses and mouse events """
    
    # Watch for keboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            # move ship to the right
            if event.key == pygame.K_RIGHT:                
                ship.moving_right = True

            # move ship to the left
            elif event.key == pygame.K_LEFT:                
                ship.moving_left = True

        elif event.type == pygame.KEYUP:

            # stop ship if right arrow key is depressed
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False

            # stop ship if left arrow key is depressed
            if event.key == pygame.K_LEFT:
                ship.moving_left = False


def update_screen(ai_settings, screen, ship):
    """ Update images on screen and flip to the new screen """
    # Redraw the screen during each pass thorugh the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()    
