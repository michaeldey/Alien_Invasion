class GameStats():
    """ Track statistics for alien invasion """

    def __init__(self, ai_settings):
        """ Initialize statistics """
        self.ai_settings = ai_settings
        self.reset_stats()

        # start alien invasion in an active state
        self.game_active = True

    def reset_stats(self):
        """ Initialize statistics that can chage during the game """
        self.ships_left= self.ai_settings.ship_limit
