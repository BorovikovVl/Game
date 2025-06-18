import pygame

class Level:
    def __init__(self, aliens_count, asteroids_count, target_aliens, target_boss, survival_time=0):
        self.aliens_count = aliens_count
        self.asteroids_count = asteroids_count
        self.target_aliens = target_aliens
        self.target_boss = target_boss
        self.survival_time = survival_time

levels = [
    Level(aliens_count=5, asteroids_count=5, target_aliens=25, target_boss=1),  # Уровень 1
    Level(aliens_count=10, asteroids_count=3, target_aliens=70, target_boss=2),  # Уровень 2
    Level(aliens_count=16, asteroids_count=7, target_aliens=0, target_boss=0, survival_time=60)  # Уровень 3
]