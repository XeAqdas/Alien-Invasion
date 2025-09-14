class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        
        # For gradient background
        self.bg_top_color = (135, 206, 250)   # Light Sky Blue
        self.bg_bottom_color = (25, 25, 112)  # Midnight Blue
        self.ship_speed = 5
        self.ship_limit = 3
        self.bg_color = (215,215,215)
        self.font_path = 'fonts/Roboto-Regular.ttf' # Path to a TTF font file
        
        #Bullet settings
        self.bullet_speed = 8
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 215, 0)  # Gold (high contrast and eye-catching)
        self.bullets_allowed = 10  # Maximum number of bullets on screen at a time
        
        #Alien Settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 left
        self.fleet_direction = 1
        
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 2
        self.bullet_speed = 8
        self.alien_speed = 2.0
        self.fleet_direction = 1
        self.alien_points = 1
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)