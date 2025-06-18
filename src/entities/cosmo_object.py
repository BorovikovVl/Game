import pygame
import random

class Cosmo(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Cosmo, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('assets/image/alien.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 0.3  # Начальная скорость

    def update(self, speed=0.1):
        """Обновление позиции пришельца"""
        self.speed = speed  # Обновляем скорость
        self.rect.y += self.speed

    def over_screen(self):
        """Проверка выхода за экран"""
        return self.rect.top > self.screen_rect.bottom

    def draw(self):
        """Отрисовка пришельца"""
        self.screen.blit(self.image, self.rect)