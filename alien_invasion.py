import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    
    #initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make a play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #Make a ship
    ship = Ship(ai_settings, screen)

    # Make group for bullets
    bullets = Group()
 
    # Make an alien group and fleet
    aliens = Group()   
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Set the background color
    bg_color = (230, 230, 230)

    
    # Start the main loop for the game.
    while True:

        # Watch for keboard and mouse events
        gf.check_events(ai_settings, screen, stats, play_button, ship,
                 aliens, bullets)

        if stats.game_active:
            #update the entities on screen
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,
                ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship,
                aliens, bullets)

        # Redraw the screen
        gf.update_screen(ai_settings, screen, stats, sb, ship,
            aliens, bullets, play_button)

run_game()
