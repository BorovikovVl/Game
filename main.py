import pygame, controls
from starship import Starship
from pygame.sprite import Group
from stats import Stats
from scores import Scores
def run():

    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('Starship')
    bg_color = (13, 2, 24)
    starship = Starship(screen)
    bullets = Group()
    asteriods = Group()
    controls.create_asteroids(screen, asteriods)
    stats = Stats()
    real_score = Scores(screen, stats)

    while True:
        controls.events(screen, starship, bullets)
        if stats.run_game == True:
            starship.update_starship()
            controls.update(bg_color, stats, real_score, screen, starship, asteriods, bullets)
            controls.update_bullets(screen, stats, real_score, asteriods, bullets)
            controls.update_asteroids(starship, asteriods, real_score, stats, screen, bullets)
run()

