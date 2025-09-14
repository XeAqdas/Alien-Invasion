import pygame
from pygame.sprite import Sprite

#Initialize the ship class
class Ship(Sprite):
    def __init__(self, ai_game): #2nd argument is an instance of AlienInvasion | go to AlineInvasion class & see "self.ship = Ship(self)" Line 22
        
        super().__init__()
        self.screen = ai_game.screen #Setting the screen attribute so that we can access it eassily in all methods
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #Getting the rectangle of the screen to position the ship correctly
        
        self.image = pygame.image.load('D:\Alien Invasion\Images\Ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)  # Store a decimal value for the ship's horizontal position
        
        #Movement flag; starting with ship not moving
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
            
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        
    def centre_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)