class Settings:
    """class for saving all gema's settings"""

    def __init__(self):
        """intialize game's settings"""
        # Screen settings
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (0, 191, 255)
        
        self.bullet_speed = 5.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        self.alien_speed = 1.0
        self.fleet_drop_speed = 8

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        
        # fleet_direction 1 means movement right; -1 -- left.
        self.fleet_direction = 1
        self.ship_limit = 3

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.2

        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
