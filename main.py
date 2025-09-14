import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullets import Bullet
from alien import Alien
from button import Button


#Class to manage game assets
class AlienInvasion:
    def __init__(self):
        
        #Initializing the game
        pygame.init() 
        self.clock = pygame.time.Clock() #Manage fps
        #setting dimesnions of game window
        self.settings = Settings() #Instance of Settings class
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) 
        pygame.display.set_caption("Alien Invasion")
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        #Setting Game visuals
        pygame.display.set_caption("Alien Invasion")
        self.bg_color = (230, 230, 230)
        
        self.stats = GameStats(self) #Instance of GameStats class and we pass current instance of AlienInvasion to the GameStats
        self.sb = Scoreboard(self)
        self.ship = Ship(self) #Instance of Ship class and we pass current instance of AlienInvasion to the Ship
        self.bullets = pygame.sprite.Group() # Group to hold bullets
        self.aliens = pygame.sprite.Group()  # Group to hold aliens
        self._create_fleet()
        
        self.firing = False  # Flag for holding spacebar
        self.last_shot_time = 0  # For cooldown
        self.shot_cooldown = 200  # milliseconds between bullets i,e, 5 bullets per second

        self.game_active = False  # Start game in an inactive state
        self.play_button = Button(self,"Play") #Make play button
        
    def run_game(self):
        #Run the main loop for the game
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._handle_continuous_firing()
                self._update_bullets()
                # print(f"Bullets on screen: {len(self.bullets)}")  # Debugging line
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60) # 60 fps
    
    def _check_events(self):
        #look for keyboard and mouse activiy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button (self, mouse_pos):
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats() #Reset the current game stats to begin new if player plays again
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.centre_ship()
                    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.firing = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_q:
            sys.exit()
                
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.firing = False
            
    def _handle_continuous_firing(self):
        if self.firing:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shot_cooldown:
                self._fire_bullet()
                self.last_shot_time = current_time

            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
       #Update bullet positions
        self.bullets.update()
        #Remove bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        #Check if bullets and aliens collide, if so then get rid of them
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
        
        if not self.aliens:  # If all aliens are destroyed
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            
    def _ship_hit(self):
        """Respond to the ship being hit by an aline"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.centre_ship()
            
            sleep(1) #pause
        else:
            self.game_active = False
            
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of the aliens."""
        self._check_fleet_edges()
        self.aliens.update()
        
        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom()
                
    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self) #Instance of Alien class
        #Spacing between aliens is one alien width and one alien height
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < self.settings.screen_height - 2*alien_height:
            while current_x < self.settings.screen_width - 2*alien_width:
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            #Finish the row and move to the next row
            current_x = alien_width
            current_y += 2*alien_height
            
    def _check_aliens_bottom (self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit() #Not in actual but just treat it like that
                break
            
    def _create_alien(self, x_position,y_position):
        """"Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien) # Add the alien to the group
        
    def _check_fleet_edges(self):
        """Respond appropiately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 #Note it is *=

    def _update_screen(self):
        #Load the visuals    
        draw_vertical_gradient(self.screen, self.settings.bg_top_color, self.settings.bg_bottom_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() #Draw the ship on the screen
        self.aliens.draw(self.screen)
        
        self.sb.show_score() #Draw the score info
        
        if not self.game_active:
            self.play_button.draw_button()
            
        #Redraw the screen during each pass through the loop.
        pygame.display.flip()
        
def draw_vertical_gradient(screen, top_color, bottom_color):
    height = screen.get_height()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()