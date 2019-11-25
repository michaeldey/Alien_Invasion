import sys
import pygame
from alien import Alien
from bullet import Bullet
from time import sleep

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
        fire_bullet(ai_settings, screen, ship, bullets)

    # end the game if the player hits 'q'
    elif event.key == pygame.K_q:
        quit_game()

def check_keyup_events(event, ship):
    # stop ship if right arrow key is depressed
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    # stop ship if left arrow key is depressed
    if event.key == pygame.K_LEFT:
        ship.moving_left = False    

def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit not reached yet """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)    

def check_events(ai_settings, screen, stats, play_button, ship,
                 aliens, bullets):
    """ Respond to keypresses and mouse events """
    
    # Watch for keboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    
    """ Start a new game when the player clicks play """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
         # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Reset game settings
        ai_settings.initialize_dynamic_settings()

        # Make mouse cursor invisible
        pygame.mouse.set_visible(False)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                  play_button):
    """ Update images on screen and flip to the new screen """

    # Redraw the screen during each pass thorugh the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Redraw ship
    ship.blitme()

    # Redraw aliens
    aliens.draw(screen)

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()    

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """ Update position of bullets and get rid of old bullets """
    # update bullet positions
    bullets.update()

    # get rid of bullets that have dissapeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # check if the bullets hit any aliens
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """ Respond to bullet-alien collisions """
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Destroy existing bullets, speed up game, and create a new fleet
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """ Determine the number of aliens that fit in a row """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """ Determine the number of rows of aliens that fit on screen """
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it in the row """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create a full fleet of aliens """
    
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)       

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """ Check if any aliens have reached the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if a ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

# Update the alien positions
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """ check if the fleet is at an edge, and
        update the positions of all aliens in the fleet """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

# What happens if the alien fleet hits the edge of screen
def check_fleet_edges(ai_settings, aliens):
    """ Respond appropriately if any aliens have reached an edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

# Change the fleet direction
def change_fleet_direction(ai_settings, aliens):
    """ Drop the entire fleet and change the fleet's direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

# Respond to player ship getting hit by alien
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """ Respond to ship being hit by alien """
    # Decriment ships left
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause the game
        sleep(0.5)

    else:
        stats.game_active = False

        # Make mouse visible again
        pygame.mouse.set_visible(True)
       
def quit_game():
    """ An easy function to end the game """
    pygame.quit()
    sys.exit()
