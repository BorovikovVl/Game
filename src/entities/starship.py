import pygame
from pygame.sprite import Sprite

class Starship(Sprite):
    '''инициализация кораблся'''
    def __init__(self, screen):
        super(Starship, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('assets/image/starship (1).png').convert_alpha()
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
        self.shield_active = False
        self.shield_timer = 0
        self.fire_rate_boost = False
        self.fire_rate_timer = 0
        self.fire_rate_delay = 500
        self.initial_lives = 3
        self.game = None

    def output(self):
        '''отрисовка'''
        if self.shield_active:
            shield_image = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            pygame.draw.circle(shield_image, (0, 0, 255, 100), (self.rect.width // 2 + 5, self.rect.height // 2 + 5), 20, 2)
            self.screen.blit(shield_image, (self.rect.x - 5, self.rect.y - 5))
        self.screen.blit(self.image, self.rect)

    def update_starship(self):
        '''передвижение'''
        if self.mright and self.rect.right < self.screen_rect.right:
            self.centerx += 4
        if self.mleft and self.rect.left > self.screen_rect.left:
            self.centerx -= 4
        if self.mup and self.rect.top > self.screen_rect.top:
            self.centery -= 4
        if self.mdown and self.rect.bottom < self.screen_rect.bottom:
            self.centery += 4

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def create_starship(self):
        '''создание после столкновения'''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def reset_position(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        self.hide_timer = pygame.time.get_ticks()
        self.shield_active = False

    def apply_bonus(self, bonus_type, stats):
        '''бонусы'''
        current_time = pygame.time.get_ticks()
        if bonus_type == 'shield':
            self.shield_active = True
            self.shield_timer = current_time + 5000
        elif bonus_type == 'extra_life':
            if stats.starship_left < self.initial_lives:
                stats.starship_left += 1
                print(f"Extra life added! Lives: {stats.starship_left}")
        elif bonus_type == 'fire_rate_boost':
            self.fire_rate_boost = True
            self.fire_rate_timer = current_time + 10000
            self.fire_rate_delay = 30