import pygame


class Bullet_2(pygame.sprite.Sprite):
    def __init__(self, screen, source, is_boss=False):
        """создаем пулю"""
        super(Bullet_2, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 4, 14)
        self.color = 200, 200, 200  # Чуть темнее для отличия
        self.speed = 7
        self.direction = 1 if is_boss else -1  # 1 для босса (вниз), -1 для корабля (вверх)

        # Позиционирование в зависимости от источника
        if is_boss:
            self.rect.centerx = source.rect.centerx + 105  # Смещение для второй пули
            self.rect.top = source.rect.bottom  # Пуля стартует снизу босса
        else:
            self.rect.centerx = source.rect.centerx + 17
            self.rect.top = source.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """перемещение пули"""
        self.y += self.speed * self.direction  # Движение в зависимости от направления
        self.rect.y = self.y

    def draw_bullet(self):
        """рисование пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)