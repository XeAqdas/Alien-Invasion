import pygame.font

class Button:
    def __init__(self, ai_game,msg):
        """Initialize Button Attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Set Dimensions
        self.width, self.height = 200, 50
        self.button_colour = (0,255,0)
        self.text_colour = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Build the buttons rect obj and centre it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        # Prep the button only once
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Draw blank button and then draw the message"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)