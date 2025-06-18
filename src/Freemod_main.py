import pygame
import random
from pygame.sprite import Group

# Импорты из src.entities
from src.entities.starship import Starship
from src.entities.bonus import Bonus

# Импорты из src.utils
from src.utils.stats import Stats
from src.utils.scores import Scores
from src.utils.music import AudioManager
from src.utils.controls import Controls, BossManager

# Импорты из src.screens
from src.screens.game_over_screen import Game_over
from src.screens.start_menu import Menu

pygame.init()
screen = pygame.display.set_mode((600, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Starship')
controls = Controls()

class FreeModeGame:
    '''Инициализация свободной игры'''
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bg_image = pygame.image.load('assets/image/back-norm.png')  # Исправлен путь
        self.bg_image = pygame.transform.scale(self.bg_image, (600, 800))
        self.stats = Stats()
        self.starship = Starship(screen)
        self.starship.game = self
        self.bullets = Group()
        self.aliens = Group()
        self.asteroids = Group()
        self.real_score = Scores(screen, self.stats)
        self.menu = Menu(screen)
        self.boss_manager = BossManager()
        self.score = Scores(screen, self.stats)  # Убрано дублирование, если не нужно
        self.game_over_scr = Game_over(screen)
        self.audio = AudioManager()
        self.load_resources()
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()
        self.alien_spawn_timer = 0
        self.alien_spawn_delay = 2500
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_delay = 4500
        self.starship_speed = 0.5
        self.alien_speed = 4
        self.asteroid_speed = 4
        self.bullet_speed = 10
        self.task_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.last_score = -1
        self.music_enabled = True

    def load_resources(self):
        self.audio.load_music('menu', 'assets/sounds/menu-base.mp3')  # Исправлен путь
        self.audio.load_music('game', 'assets/sounds/pixel.wav')
        self.audio.load_music('click', 'assets/sounds/menu.mp3')  # Исправлен путь
        self.audio.set_volume(0.5)

    def show_task(self):
        font = pygame.font.SysFont(None, 36)
        if self.last_score != self.stats.score:
            score_text = font.render(f"Очки: {self.stats.score}", True, (255, 255, 255))
            self.task_surface.fill((0, 0, 0, 0))
            self.task_surface.blit(score_text, (0, 10))
            self.last_score = self.stats.score
        self.screen.blit(self.task_surface, (10, 10))

    def run(self):
        self.audio.play_music('game') if self.music_enabled else self.audio.stop_music()
        running = True
        paused = False

        while running:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - self.last_time
            self.last_time = current_time

            self.clock.tick(260)

            if not paused:
                result = controls.events(self.screen, self.starship, self.bullets)
                if result == 'quit':
                    self.audio.stop_music()
                    return 'quit'
                elif result == 'pause':
                    paused = True
                    self.audio.play_music('menu')
                    result = self.menu.pause_menu()
                    if result == 'menu':
                        self.audio.stop_music()
                        return 'menu'
                    elif result == 'quit':
                        self.audio.stop_music()
                        return 'quit'
                    else:
                        paused = False

                self.starship.update_starship()
                self.screen.blit(self.bg_image, (0, 0))
                controls.update(
                    self.bg_image,
                    self.stats,
                    self.score,
                    self.screen,
                    self.starship,
                    self.aliens,
                    self.asteroids,
                    self.bullets,
                    self.boss_manager
                )
                if self.stats.run_game:
                    self._update_game(delta_time)

            self.show_task()
            pygame.display.flip()

            if self.stats.starship_left <= 0:
                running = False

        return self._game_over()

    def _update_game(self, delta_time):
        self.starship.speed = self.starship_speed
        self.starship.update_starship()

        controls.update_bullets(
            self.screen,
            self.stats,
            self.real_score,
            self.aliens,
            self.asteroids,
            self.bullets,
            self.boss_manager,
            starship=self.starship
        )
        controls.update_aliens(
            self.starship,
            self.aliens,
            self.real_score,
            self.stats,
            self.screen,
            self.bullets,
            self.asteroids,
            self.boss_manager,
            aliens_per_level={},
            current_level=0,
            speed=self.alien_speed
        )
        controls.update_asteroids(
            self.starship,
            self.aliens,
            self.real_score,
            self.stats,
            self.screen,
            self.bullets,
            self.asteroids,
            self.boss_manager,
            asteroids_per_level={},
            current_level=0,
            speed=self.asteroid_speed
        )
        result = self.boss_manager.handle_boss(self.screen, self.stats, self.bullets, self.starship)

        self.alien_spawn_timer += delta_time / 1000
        if self.alien_spawn_timer >= self.alien_spawn_delay / 1000:
            self.alien_spawn_timer = 0
            controls.create_aliens(self.screen, self.aliens, self.boss_manager)
            self.alien_spawn_delay = random.randint(500, 1500)
        self.asteroid_spawn_timer += delta_time / 1000
        if self.asteroid_spawn_timer >= self.asteroid_spawn_delay / 1000:
            self.asteroid_spawn_timer = 0
            controls.create_asteroids(self.screen, self.asteroids, self.boss_manager)
            self.asteroid_spawn_delay = random.randint(1500, 3000)

        for alien in self.aliens.copy():
            if isinstance(alien, Bonus) and pygame.sprite.collide_rect(self.starship, alien):
                self.starship.apply_bonus(alien.bonus_type, self.stats)
                alien.kill()

        current_time = pygame.time.get_ticks()
        if self.starship.shield_active and current_time > self.starship.shield_timer:
            self.starship.shield_active = False
        if self.starship.fire_rate_boost and current_time > self.starship.fire_rate_timer:
            self.starship.fire_rate_boost = False
            self.starship.fire_rate_delay = 500

        if result == "HIT":
            controls.starship_destroy(self.stats, self.screen, self.starship, self.real_score, self.bullets, self.aliens,
                                      self.game_over_scr, self.asteroids, self.boss_manager, aliens_per_level={},
                                      current_level=0, asteroids_per_level={})

    def _game_over(self):
        self.audio.stop_music()
        self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = self.screen_rect.center
        score_text = pygame.font.SysFont(None, 48).render(
            f"Final Score: {self.stats.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.centerx = self.screen_rect.centerx
        score_rect.top = game_over_rect.bottom + 20
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        return 'menu'

if __name__ == "__main__":
    game = FreeModeGame(screen)
    result = game.run()
    pygame.quit()