import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, source, is_boss=False):
        """создаем пулю"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 4, 14)
        self.color = 250, 250, 250
        self.speed = 7
        self.direction = 1 if is_boss else -1  # 1 для босса (вниз), -1 для корабля (вверх)

        # Позиционирование в зависимости от источника
        if is_boss:
            self.rect.centerx = source.rect.centerx - 104
            self.rect.top = source.rect.bottom  # Пуля стартует снизу босса
        else:  # Предполагаем, что источник — корабль (Starship)
            self.rect.centerx = source.rect.centerx - 16
            self.rect.top = source.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """перемещение пули"""
        self.y += self.speed * self.direction  # Движение в зависимости от направления
        self.rect.y = self.y

    def draw_bullet(self):
        """рисование пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)