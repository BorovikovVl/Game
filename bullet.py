import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self,screen, starship):
        """создаем пулю"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 4, 14)
        self.color = 250, 250, 250
        self.speed = 1.4
        self.rect.centerx = starship.rect.centerx - 16
        self.rect.top = starship.rect.top
        self.y = float(self.rect.y)


    def update(self):
        """перемещение пули"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """рисование пули"""
        pygame.draw.rect(self.screen, self.color, self.rect)

