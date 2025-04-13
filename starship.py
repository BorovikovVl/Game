import pygame
from pygame.sprite import Sprite

class Starship(Sprite):

    def __init__(self, screen):
        """инициализация корабля"""
        super(Starship, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('image/starship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.mright = False
        self.mleft = False
        self.mup = False
        self.mdown = False
    def output(self):
        """рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update_starship(self):
        """обновление движения корабля"""
        if self.mright == True and self.rect.right < self.screen_rect.right:
            self.centerx += 0.5
        if self.mleft == True and self.rect.left > self.screen_rect.left:
            self.centerx -= 0.5
        if self.mup == True and self.rect.top > self.screen_rect.top:
            self.centery -= 0.5
        if self.mdown == True and self.rect.bottom < self.screen_rect.bottom:
            self.centery += 0.5

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def create_starship(self):
        """размещает корбаль внизу"""
        self.center = self.screen_rect.centerx