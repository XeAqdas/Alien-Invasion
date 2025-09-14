class GameStats:
    """Track statistics for Alien Invasion"""
    
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.level = 1
        self.high_score = 0
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        