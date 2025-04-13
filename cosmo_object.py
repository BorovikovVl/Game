import pygame

class Cosmo(pygame.sprite.Sprite):
    """класс одного астероида"""

    def __init__(self, screen):
        """"""
        super(Cosmo, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('image/asteriod.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self):
        """вывод астероида на экран"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """перемещение астероидов"""
        self.y += 0.1
        self.rect.y = self.y
