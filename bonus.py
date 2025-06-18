import pygame
import random

class Bonus(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, bonus_type):
        super(Bonus, self).__init__()
        self.screen = screen
        self.bonus_type = bonus_type  # 'shield', 'extra_life', 'fire_rate_boost'
        self.image = {
            'shield': pygame.image.load('image/shield (2).png').convert_alpha(),
            'extra_life': pygame.image.load('image/new_red_heart.png').convert_alpha(),
            'fire_rate_boost': pygame.image.load('image/bonus_fast_bullet.png').convert_alpha()
        }[bonus_type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.screen_rect = screen.get_rect()

    def update(self, speed=1):
        self.speed = speed
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_height():
            self.kill()

    def over_screen(self):
        return self.rect.top > self.screen_rect.bottom

    def draw(self):
        self.screen.blit(self.image, self.rect)