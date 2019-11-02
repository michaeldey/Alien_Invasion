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
            if event.key == pygame.K_RIGHT:
                # move ship to the right
                ship.rect.centerx += 1

def update_screen(ai_settings, screen, ship):
    """ Update images on screen and flip to the new screen """
    # Redraw the screen during each pass thorugh the loop.
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()    
