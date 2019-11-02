import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    
    #initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make a ship
    ship = Ship(ai_settings, screen)

    # Make group for bullets
    bullets = Group()

    # Set the background color
    bg_color = (230, 230, 230)
 

    # Start the main loop for the game.
    while True:

        # Watch for keboard and mouse events
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()

        #update the images on the screen
        bullets.update()
        gf.update_screen(ai_settings, screen, ship, bullets)
        
run_game()
