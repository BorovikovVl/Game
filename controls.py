import pygame
from bullet import Bullet
from bullet_2 import Bullet_2
from cosmo_object import Cosmo
from asteroid import Asteroids
from music import AudioManager
from boss import Boss
import time
import random
from bonus import Bonus

all_sprites = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

class Controls:
    '''инициализация класса для всех действий в игре'''
    def __init__(self):
        self.spawn_timer = 0
        self.current_time = 0

    def events(self, screen, starship, bullets):
        current_time = pygame.time.get_ticks()
        last_shot = getattr(starship, 'last_shot', 0) # пытается найти атрибут last_shot в объекте starship
        shoot_delay = starship.fire_rate_delay if starship.fire_rate_boost else 500

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AudioManager.stop_music()
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'pause'
                elif event.key == pygame.K_d:
                    starship.mright = True
                elif event.key == pygame.K_a:
                    starship.mleft = True
                elif event.key == pygame.K_w:
                    starship.mup = True
                elif event.key == pygame.K_s:
                    starship.mdown = True
                elif event.key == pygame.K_SPACE and current_time - last_shot >= shoot_delay:
                    new_bullet = Bullet(screen, starship)
                    new_bullet_2 = Bullet_2(screen, starship)
                    bullets.add(new_bullet)
                    bullets.add(new_bullet_2)
                    starship.last_shot = current_time
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    starship.mright = False
                elif event.key == pygame.K_a:
                    starship.mleft = False
                elif event.key == pygame.K_w:
                    starship.mup = False
                elif event.key == pygame.K_s:
                    starship.mdown = False
        return None

    def update(self, bg_color, stats, score, screen, starship, aliens, asteroids, bullets, boss_manager):
        screen.blit(bg_color, (0, 0))
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        starship.output()
        aliens.draw(screen)
        asteroids.draw(screen)
        if boss_manager and hasattr(boss_manager, 'boss') and boss_manager.boss:
            boss_manager.boss.update()  # Обновляем движение босса
            boss_manager.boss.draw(screen)  # Отрисовываем босса и здоровье
        pygame.display.flip()

    def update_bullets(self, screen, stats, real_score, aliens_group, asteroids, bullets, boss_manager, starship=None):
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.top >= screen.get_height():
                bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(bullets, aliens_group, True, True)
        if collisions:
            total_killed = 0
            for aliens in collisions.values():
                stats.score += 10 * len(aliens)
                total_killed += sum(1 for alien in aliens if isinstance(alien, Cosmo))
            real_score.image_score()
            self.check_best_score(stats, real_score)
            real_score.image_starships()
            if random.random() < 0.2:
                self.create_bonus(screen, boss_manager, aliens_group)
            for alien in aliens_group.copy():
                if isinstance(alien, Bonus):
                    bullet_collisions = pygame.sprite.spritecollide(alien, bullets, True)
                    if bullet_collisions and starship:
                        starship.apply_bonus(alien.bonus_type, stats)
                        alien.kill()
            return total_killed
        return 0  # Возвращаем 0, если коллизий нет

    def starship_destroy(self, stats, screen, starship, real_score, bullets, aliens, game_over_scr, asteroids,
                         boss_manager, aliens_per_level, current_level, asteroids_per_level=None):
        if not starship.shield_active:
            if stats.starship_left > 0:
                stats.starship_left -= 1
                starship.create_starship()
                aliens.empty()
                asteroids.empty()
                bullets.empty()
                if not boss_manager.is_boss_active():
                    aliens_per_level = aliens_per_level or {1: 20, 2: 10}
                    asteroids_per_level = asteroids_per_level or {1: 0, 2: 2}
                    target_aliens = aliens_per_level.get(current_level, 5)
                    for _ in range(target_aliens):
                        if len(aliens) < target_aliens:
                            self.create_aliens(screen, aliens, boss_manager)
                    if current_level >= 2 or current_level == 0:
                        num_asteroids = random.randint(3, 4)
                        for _ in range(num_asteroids):
                            if len(asteroids) < num_asteroids:
                                self.create_asteroids(screen, asteroids, boss_manager)
                starship.reset_position()
                time.sleep(1)
            else:
                stats.run_game = False
                game_over_scr.show_game_over_screen()

    def update_aliens(self, starship, aliens, real_score, stats, screen, bullets, asteroids,
                      boss_manager, aliens_per_level, current_level, speed=1):
        aliens.update(speed=speed)
        for alien in aliens.copy():
            if isinstance(alien, Cosmo) and alien.over_screen():
                aliens.remove(alien)
        if pygame.sprite.spritecollideany(starship, aliens):
            collided = pygame.sprite.spritecollideany(starship, aliens)
            if collided and isinstance(collided, Cosmo):
                self.starship_destroy(stats, screen, starship, real_score, bullets, aliens, None, asteroids,
                                      boss_manager, aliens_per_level, current_level)

    def update_asteroids(self, starship, aliens, real_score, stats, screen, bullets, asteroids,
                         boss_manager, asteroids_per_level, current_level, speed=1):
        asteroids.update(speed=speed)
        if pygame.sprite.spritecollideany(starship, asteroids):
            self.starship_destroy(stats, screen, starship, real_score, bullets, aliens, None, asteroids,
                                  boss_manager, aliens_per_level=None, current_level=current_level, asteroids_per_level=asteroids_per_level)

    def aliens_check(self, stats, screen, starship, real_score, aliens, bullets, boss_manager):
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
            if isinstance(alien, Cosmo) and alien.rect.bottom >= screen_rect.bottom:
                self.starship_destroy(stats, screen, starship, real_score, bullets, aliens, None, boss_manager,
                                      aliens_per_level=None, current_level=0, asteroids_per_level=None)

    def create_aliens(self, screen, aliens, boss_manager):
        if boss_manager is None or not boss_manager.is_boss_active():
            num_aliens = random.randint(1, 4)
            for _ in range(num_aliens):
                alien = Cosmo(screen)
                aliens.add(alien)

    def create_asteroids(self, screen, asteroids, boss_manager=None):
        if boss_manager is None or not boss_manager.is_boss_active():
            x = random.randint(0, screen.get_width())
            y = -100
            asteroid = Asteroids(x, y)
            asteroids.add(asteroid)

    def create_bonus(self, screen, boss_manager, aliens_group):
        if boss_manager is None or not boss_manager.is_boss_active():
            x = random.randint(0, screen.get_width())
            y = -50
            bonus_type = random.choice(['shield', 'extra_life', 'fire_rate_boost'])
            bonus = Bonus(screen, x, y, bonus_type)
            aliens_group.add(bonus)

    def check_best_score(self, stats, real_score):
        if stats.score > stats.best_score:
            stats.best_score = stats.score
            real_score.image_best_score()
            with open('the_best_score.txt', 'w') as f:
                f.write(str(stats.best_score))

class BossManager:
    '''инициализация класса для работы босса'''
    def __init__(self):
        self.boss = None
        self.spawn_threshold = 500
        self.next_spawn_score = 500
        self.is_active = False

    def handle_boss(self, screen, stats, bullets, starship):
        if stats.score >= self.next_spawn_score and self.boss is None:
            self.boss = Boss(screen)
            self.next_spawn_score += self.spawn_threshold
            self.is_active = False
            print("Boss spawned")
        if self.boss:
            if not self.boss.has_stopped:
                self.boss.rect.y += self.boss.speed
                if self.boss.rect.top >= self.boss.stop_y:
                    self.boss.has_stopped = True
                    self.is_active = True
                    print("Boss has stopped")
            if self.boss.has_stopped:
                self.boss.shoot()
                # Обновляем позиции пуль босса
                for bullet in self.boss.bullets.sprites():
                    bullet.rect.y += 5  # Скорость движения вниз
                    if bullet.rect.bottom >= screen.get_height():
                        self.boss.bullets.remove(bullet)
                if pygame.sprite.spritecollideany(starship, self.boss.bullets):
                    for bullet in self.boss.bullets.copy():
                        if pygame.sprite.collide_rect(starship, bullet):
                            self.boss.bullets.remove(bullet)
                            return "HIT"
                hits = pygame.sprite.spritecollide(self.boss, bullets, True)
                print(f"Boss HP: {self.boss.hp}, Hits: {len(hits)}")
                for _ in hits:
                    self.boss.hp -= 1
                    if self.boss.hp <= 0:
                        stats.score += 200
                        self.boss = None
                        print("Boss defeated")
                        return "DEFEATED"
        return None

    def is_boss_active(self):
        return self.boss is not None and self.boss.has_stopped

    def draw(self, screen):
        if self.boss:
            self.boss.draw(screen)  # Делегируем отрисовку боссу

class FreeModeControls:
    pass