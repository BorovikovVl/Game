import pygame
from bullet import Bullet
from bullet_2 import Bullet_2
import random

class Boss(pygame.sprite.Sprite):
    '''создание босса'''
    def __init__(self, screen):
        super(Boss).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Загрузка изображения с гарантированным fallback
        self.image = pygame.image.load('image/boss.png').convert_alpha()
        self.rect = self.image.get_rect(centerx=self.screen_rect.centerx, top=-300)

        # Настройки движения
        self.speed = 3
        self.stop_y = 150  # Высота остановки
        self.has_stopped = False
        self.move_direction = 2  # 1 для вправо, -1 для влево
        self.move_speed = 4
        self.move_boundary = 250  # Амплитуда горизонтального движения

        # Параметры здоровья
        self.max_hp = 50
        self.hp = self.max_hp
        self.last_hit_time = 0

        # Пули босса
        self.bullets = pygame.sprite.Group()
        self.shoot_timer = 0
        self.shoot_delay = 50  # Задержка между выстрелами в миллисекундах (0.3 секунды)

    def update(self):
        """Обновление позиции босса и пуль"""
        if not self.has_stopped:
            self.rect.y += self.speed
            if self.rect.top >= self.stop_y:
                self.rect.top = self.stop_y
                self.has_stopped = True
                print("Boss has stopped, ready to shoot")
        else:
            # Горизонтальное движение влево-вправо
            self.rect.x += self.move_speed * self.move_direction
            if self.rect.left <= self.screen_rect.centerx - self.move_boundary or self.rect.right >= self.screen_rect.centerx + self.move_boundary:
                self.move_direction *= -1  # Меняем направление

        # Обновление пуль босса
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom >= self.screen_rect.bottom:
                self.bullets.remove(bullet)

    def shoot(self):
        """Стрельба босса"""
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_delay and self.has_stopped:
            print(f"Boss shooting at time {current_time}")
            # Создаём пули с небольшим разбросом
            bullet = Bullet(self.screen, self, is_boss=True)
            bullet_2 = Bullet_2(self.screen, self, is_boss=True)
            bullet.rect.x = self.rect.centerx - 100  # Смещаем первую пулю влево
            bullet_2.rect.x = self.rect.centerx + 100  # Смещаем вторую пулю вправо
            self.bullets.add(bullet, bullet_2)
            self.shoot_timer = current_time
            self.shoot_delay = random.randint(1000, 3000)  # Случайная задержка для следующего выстрела

    def draw(self, screen):
        """Отрисовка босса, его пуль и полоски здоровья"""
        screen.blit(self.image, self.rect)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Полоска здоровья
        health_bar_width = 100
        health_bar_height = 10
        health_ratio = self.hp / self.max_hp
        health_bar_x = self.rect.centerx - health_bar_width // 2
        health_bar_y = self.rect.top - 20
        # Фон полоски (красный)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        # Заполнение здоровья (зеленое)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))