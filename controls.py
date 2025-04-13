import pygame, sys
from bullet import Bullet
from bullet_2 import Bullet_2
from cosmo_object import Cosmo
import time

def events(screen, starship, bullets):
    """обработка события"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # вправо
            if event.key == pygame.K_d:
                starship.mright = True
            # влево
            elif event.key == pygame.K_a:
                starship.mleft = True
            # вверх
            elif event.key == pygame.K_w:
                starship.mup = True
            # вниз
            elif event.key == pygame.K_s:
                starship.mdown = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, starship)
                new_bullet_2 = Bullet_2(screen, starship)
                bullets.add(new_bullet)
                bullets.add(new_bullet_2)
        elif event.type == pygame.KEYUP:
            # вправо
            if event.key == pygame.K_d:
                starship.mright = False
            # влево
            elif event.key == pygame.K_a:
                starship.mleft = False
            # вверх
            elif event.key == pygame.K_w:
                starship.mup = False
            # вниз
            elif event.key == pygame.K_s:
                starship.mdown = False

def update(bg_color, stats, score, screen, starship, asteriods, bullets):
    """обновление экрана"""
    screen.fill(bg_color)
    score.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet_2 in bullets.sprites():
        bullet_2.draw_bullet()
    starship.output()
    asteriods.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, real_score, asteroids, bullets):
    """обновляет позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    if collisions:
        for asteroids in collisions.values():
            stats.score += 10 * len(asteroids)
        real_score.image_score()
        check_best_score(stats, real_score)
        real_score.image_starships()
    if len(asteroids) == 0:
        bullets.empty()
        create_asteroids(screen, asteroids)

def starship_destroy(stats, screen, starship, real_score, bullets, asteroids):
    """столкновение"""
    if stats.starship_left > 0:
        stats.starship_left -= 1
        real_score.create_starship()
        asteroids.empty()
        bullets.empty()
        create_asteroids(screen, asteroids)
        starship.image_starships()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_asteroids(starship, asteroids, real_score, stats, screen, bullets):
    """обновляет позиции астероидов"""
    asteroids.update()
    if pygame.sprite.spritecollideany(starship, asteroids):
        starship_destroy(stats, screen, real_score, starship, bullets, asteroids)
    asteroids_check(stats, screen, real_score, starship, asteroids, bullets)

def asteroids_check(stats, screen, starship, real_score, asteroids, bullets):
    """проверка"""
    screen_rect = screen.get_rect()
    for asteroid in asteroids.sprites():
        if asteroid.rect.bottom >= screen_rect.bottom:
            starship_destroy(stats, screen, real_score, starship, bullets, asteroids)

def create_asteroids(screen, asteriods):
    """создание кучи астероидов"""
    asteriod = Cosmo(screen)
    asteriod_width = asteriod.rect.width
    number_asteriod_x = int((600 - 2 * asteriod_width) / asteriod_width)

    for asteriod_number in range(number_asteriod_x):
        asteriod = Cosmo(screen)
        asteriod.x = asteriod_width + asteriod_width * asteriod_number
        asteriod.rect.x = asteriod.x
        asteriods.add(asteriod)

def check_best_score(stats, real_score):
    if stats.score > stats.best_score:
        stats.best_score = stats.score
        real_score.image_best_score()
        with open('the_best_score.txt', 'w') as f:
            f.write(str(stats.best_score))
