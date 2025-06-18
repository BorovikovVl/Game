import pygame
import random

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Asteroids, self).__init__()
        self.image = pygame.image.load('image/asteroid_3.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.3  # Начальная скорость

    def update(self, speed=0.1):
        """Обновление позиции астероида"""
        self.speed = speed  # Обновляем скорость
        self.rect.y += self.speed

    def draw(self):
        """Отрисовка астероида"""
        screen = pygame.display.get_surface()  # Получаем текущий экран
        screen.blit(self.image, self.rect)