import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Respond to keypresses """

    # move ship to the right
    if event.key == pygame.K_RIGHT:                
        ship.moving_right = True

    # move ship to the left
    elif event.key == pygame.K_LEFT:                
        ship.moving_left = True

    # create a new bullet and add it to the bullets group
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    # stop ship if right arrow key is depressed
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    # stop ship if left arrow key is depressed
    if event.key == pygame.K_LEFT:
        ship.moving_left = False    

def check_events(ai_settings, screen, ship, bullets):
    """ Respond to keypresses and mouse events """
    
    # Watch for keboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)


        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, bullets):
    """ Update images on screen and flip to the new screen """
    # Redraw the screen during each pass thorugh the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Redraw ship
    ship.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()    
