import pygame.font
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        """індикатор руху"""

        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False

        self.ship_speed=5.5

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        
    def update(self):
        """
        Оновити поточну позицію корабля на основі
        індикатору руху.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ship_speed

        self.rect.x = self.x
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
