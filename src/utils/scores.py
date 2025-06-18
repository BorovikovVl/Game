import pygame.font
from src.entities.starship import Starship
from pygame.sprite import Group
class Scores():

    def __init__(self, screen, stats):
        """инициализируем подсчет очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 25)
        self.image_score()
        self.image_best_score()
        self.image_starships()

    def image_score(self):
        """преобразовывает текст счета в изображение"""
        self.score_img = self.font.render(str(self.stats.score), True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 50
        self.score_rect.top = 20

    def image_best_score(self):
        """преобразует рекорд в изображение"""
        self.best_score_img = self.font.render(str(self.stats.best_score), True, self.text_color, (0, 0, 0))
        self.best_score_rect = self.best_score_img.get_rect()
        self.best_score_rect.left = self.screen_rect.left + 50
        self.best_score_rect.top = 20

    def image_starships(self):
        """кол-во жизней"""
        self.starships = Group()
        for starship_number in range(self.stats.starship_left):
            starship = Starship(self.screen)
            starship.rect.x = 15 + starship_number * starship.rect.width
            starship.rect.y = 690
            self.starships.add(starship)

    def show_score(self):
        """показ счета на экране"""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.best_score_img, self.best_score_rect)
        self.starships.draw(self.screen)

