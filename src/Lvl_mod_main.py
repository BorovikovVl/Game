import pygame
import random
from pygame.sprite import Group

# Импорты из src.entities
from src.entities.starship import Starship
from src.entities.bonus import Bonus

# Импорты из src.utils
from src.utils.stats import Stats
from src.utils.levels import Level
from src.utils.levels import levels
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

class StoryGame:
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
        self.score = Scores(screen, self.stats)
        self.game_over_scr = Game_over(screen)
        self.current_level = 1
        self.MAX_LEVEL = len(levels)
        self.audio = AudioManager()
        self.volume = 1.0
        self.music_enabled = True
        self.load_resources()
        self.clock = pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()
        self.alien_spawn_timer = 0
        self.alien_spawn_delay = 2000
        self.asteroid_spawn_timer = 0
        self.asteroid_spawn_delay = 4000
        self.alien_speed = 4
        self.asteroid_speed = 4
        self.aliens_killed = 0
        self.boss_killed = 0
        self.task_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        self.last_aliens_killed = -1
        self.last_boss_killed = -1
        self.game_state = 'running'
        self.selected_mode = None
        self.level_start_time = 0
        pygame.mixer.init()

    def load_resources(self):
        print(f"Loading resources with volume: {self.volume}")
        self.audio.load_music('menu', 'assets/sounds/menu-base.mp3')  # Исправлен путь
        self.audio.load_music('game', 'assets/sounds/pixel.wav')
        self.audio.load_music('click', 'assets/sounds/pixel.wav')
        self.audio.set_volume(self.volume)
        self.dialog_sound = pygame.mixer.Sound('assets/sounds/8-bit_task.wav')  # Исправлен путь

    def show_dialog(self, level):
        self.audio.stop_music()
        print("Stopping music for dialog")
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)  # Исправлен путь
        if level == 1:
            full_text = "Уничтожь 25 пришельцев! Берегись их шатла!"
        elif level == 2:
            full_text = "Убей 70 пришельцeв и босса! Удачи, боец..."
        else:
            full_text = f"Продeржись минуту, чтобы мы вытащили тебя отсюда!"

        displayed_text = ""
        lines = []
        current_line = ""
        words = full_text.split()

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= 560:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())

        pygame.mixer.Sound.play(self.dialog_sound)

        for line in lines:
            for i, char in enumerate(line):
                displayed_text = line[:i + 1]
                text_surface = font.render(displayed_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(300, 350 + lines.index(line) * 40))
                self.screen.fill((0, 0, 0))
                for j, line_text in enumerate(lines[:lines.index(line) + 1]):
                    if j == lines.index(line):
                        line_surface = font.render(displayed_text, True, (255, 255, 255))
                    else:
                        line_surface = font.render(line_text, True, (255, 255, 255))
                    self.screen.blit(line_surface, (20, 330 + j * 40))
                pygame.display.flip()
                pygame.time.wait(100)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.screen.fill((0, 0, 0))
                        for j, line_text in enumerate(lines):
                            line_surface = font.render(line_text, True, (255, 255, 255))
                            self.screen.blit(line_surface, (20, 330 + j * 40))
                        pygame.display.flip()
                        pygame.time.wait(200)
                        break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    break

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        print(f"Playing game music after dialog for level {level}")
        self.audio.play_music('game') if self.music_enabled else self.audio.stop_music()

    def select_level(self):
        self.audio.stop_music()
        print("Playing menu music")
        self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
        while True:
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 60)

            print("Entering main menu")
            main_result = self.menu.main_menu()
            print(f"Main menu returned: {main_result}")
            if main_result == 'quit':
                return 'quit'
            elif main_result is None:
                continue
            elif isinstance(main_result, tuple) and main_result[0] == 'start':
                self.selected_mode = main_result[1]
                if self.selected_mode == 'free':
                    self.current_level = 1
                    return 'start'
                elif self.selected_mode == 'story':
                    level = self.choose_level()
                    if level:
                        self.current_level = level
                        return 'start'
            elif main_result == 'settings':
                print(f"Current volume before settings: {self.volume}")
                self.volume, self.music_enabled, action = self.menu.settings_menu(self.audio, self.volume, self.music_enabled)
                print(f"Settings returned: volume={self.volume}, music_enabled={self.music_enabled}, action={action}")
                self.audio.set_volume(self.volume)
                if self.music_enabled:
                    self.audio.stop_music()
                    print("Playing menu music after settings")
                    self.audio.play_music('menu')
                else:
                    self.audio.stop_music()
                if action == 'quit':
                    return 'quit'
                elif action == 'back_to_menu':
                    continue
            elif main_result == 'info':
                continue

    def choose_level(self):
        while True:
            self.menu.draw_background()
            font_title = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 40)
            title_text = "Select"
            title_surface = font_title.render(title_text, True, (128, 0, 255))
            title_rect = title_surface.get_rect(center=(300, 100))
            self.screen.blit(title_surface, title_rect)

            button_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 30)
            level1_rect = self._draw_level_button("Level 1", 250, 1)
            level2_rect = self._draw_level_button("Level 2", 350, 2)
            level3_rect = self._draw_level_button("Level 3", 450, 3)
            back_rect = self._draw_level_button("Back", 550, 0)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if level1_rect.collidepoint(mouse_pos):
                        return 1
                    if level2_rect.collidepoint(mouse_pos):
                        return 2
                    if level3_rect.collidepoint(mouse_pos):
                        return 3
                    if back_rect.collidepoint(mouse_pos):
                        return None

    def _draw_level_button(self, text, y, level_id):
        mouse_pos = pygame.mouse.get_pos()
        text_surf = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36).render(text, True,
                                                                                        (150, 150, 130) if self._is_hover_level(y, text) else (255, 255, 255))
        text_rect = text_surf.get_rect(center=(300, y))
        button_width = text_rect.width + 80
        button_height = text_rect.height + 20
        base_x = 300 - button_width // 2
        base_y = y - button_height // 2

        points = [(base_x + random.randint(-5, 5), base_y + random.randint(-5, 5)),
                  (base_x + button_width + random.randint(-5, 5), base_y + random.randint(-5, 5)),
                  (base_x + button_width + random.randint(-5, 5), base_y + button_height + random.randint(-5, 5)),
                  (base_x + random.randint(-5, 5), base_y + button_height + random.randint(-5, 5))]

        shadow_points = [(x + 6, y + 6) for x, y in points]
        pygame.draw.polygon(self.screen, (0, 0, 0, 150), shadow_points)

        bevel_points = [(x + 2, y + 2) for x, y in points]
        pygame.draw.polygon(self.screen, (200, 200, 200), [bevel_points[0], bevel_points[1], (bevel_points[1][0] - 2, bevel_points[1][1] + 2), (bevel_points[0][0] - 2, bevel_points[0][1] + 2)])
        pygame.draw.polygon(self.screen, (50, 50, 50), [bevel_points[2], bevel_points[3], (bevel_points[3][0] + 2, bevel_points[3][1] - 2), (bevel_points[2][0] + 2, bevel_points[2][1] - 2)])

        pygame.draw.polygon(self.screen, (100, 100, 120), points, 4)

        inner_points = [(x + 6, y + 6) for x, y in points]
        base_color = (77, 77, 77) if level_id > 0 else (255, 0, 0)
        for i in range(4):
            gradient_points = [(inner_points[0][0] + i, inner_points[0][1] + i),
                              (inner_points[1][0] - i, inner_points[1][1] + i),
                              (inner_points[2][0] - i, inner_points[2][1] - i),
                              (inner_points[3][0] + i, inner_points[3][1] - i)]
            gradient_factor = 1.0 - (i * 0.2)
            gradient_color = (int(base_color[0] * gradient_factor), int(base_color[1] * gradient_factor), int(base_color[2] * gradient_factor))
            pygame.draw.polygon(self.screen, gradient_color, gradient_points)

        self.screen.blit(text_surf, text_rect)
        return pygame.Rect(base_x, base_y, button_width, button_height)

    def _is_hover_level(self, y, text):
        text_surf = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36).render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(250, y))
        button_width = text_rect.width + 80
        button_height = text_rect.height + 20
        button_rect = pygame.Rect(250 - button_width // 2, y - button_height // 2, button_width, button_height)
        return button_rect.collidepoint(pygame.mouse.get_pos())

    def show_task(self):
        if self.game_state == 'running':
            current_level_data = levels[self.current_level - 1]  # Исправлено на Levels
            font = pygame.font.SysFont(None, 33)
            if current_level_data.survival_time > 0:
                elapsed_time = (pygame.time.get_ticks() - self.level_start_time) / 1000
                time_left = max(0, current_level_data.survival_time - elapsed_time)
                time_text = font.render(f"Время: {int(time_left)}", True, (255, 255, 255))
                self.task_surface.fill((0, 0, 0, 0))
                self.task_surface.blit(time_text, (0, 0))
            else:
                if self.last_aliens_killed != self.aliens_killed or self.last_boss_killed != self.boss_killed:
                    aliens_text = font.render(f"Пришельцы: {min(self.aliens_killed, current_level_data.target_aliens)}/{current_level_data.target_aliens}", True, (255, 255, 255))
                    boss_text = font.render(f"Босс: {self.boss_killed}/{current_level_data.target_boss}", True, (255, 255, 255))
                    self.task_surface.fill((0, 0, 0, 0))
                    self.task_surface.blit(aliens_text, (0, 0))
                    self.task_surface.blit(boss_text, (0, 40))
                    self.last_aliens_killed = self.aliens_killed
                    self.last_boss_killed = self.boss_killed
            self.screen.blit(self.task_surface, (10, 10))

    def run(self):
        result = self.select_level()
        if result == 'quit':
            return 'quit'

        self.audio.stop_music()
        print("Playing game music")
        self.audio.play_music('game') if self.music_enabled else self.audio.stop_music()
        if self.current_level in [1, 2]:
            result = self.show_dialog(self.current_level)
            if result == 'quit':
                return 'quit'
        self.load_level()
        self.game_state = 'running'

        while True:
            self.clock.tick(260)

            if self.game_state == 'running':
                result = controls.events(self.screen, self.starship, self.bullets)
                if result == 'quit':
                    self.audio.stop_music()
                    return 'quit'
                elif result == 'pause':
                    self.audio.play_music('click')
                    result = self.menu.pause_menu()
                    if result == 'menu':
                        self.audio.stop_music()
                        print("Returning to menu, playing menu music")
                        self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
                        return 'menu'
                    elif result == 'quit':
                        self.audio.stop_music()
                        return 'quit'

                self.starship.update_starship()
                self.screen.blit(self.bg_image, (0, 0))
                controls.update(self.bg_image, self.stats, self.score, self.screen, self.starship, self.aliens, self.asteroids, self.bullets, self.boss_manager)
                self._update_game()

            self.show_task()
            pygame.display.flip()

            starship_lives = self.stats.starship_left if self.stats.starship_left is not None else 0
            if int(starship_lives) <= 0:
                self.game_state = 'game_over'
                result = self._game_over()
                if result == 'menu':
                    self.audio.stop_music()
                    print("Game over, playing menu music")
                    self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
                    return 'menu'
                elif result == 'restart':
                    self.aliens.empty()
                    self.asteroids.empty()
                    self.bullets.empty()
                    self.stats.reset_stats()
                    self.load_level()
                    self.game_state = 'running'
                    continue

            if self.game_state == 'victory':
                current_level_data = levels[self.current_level - 1]
                final_aliens_killed = self.aliens_killed
                final_boss_killed = self.boss_killed
                result = self._victory_screen(self.current_level, final_aliens_killed, final_boss_killed, current_level_data.target_aliens, current_level_data.target_boss)
                if result == 'menu':
                    self.audio.stop_music()
                    print("Victory, playing menu music")
                    self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
                    return 'menu'
                elif result == 'start' and self.current_level < self.MAX_LEVEL:
                    self.aliens.empty()
                    self.asteroids.empty()
                    self.bullets.empty()
                    self.game_state = 'running'
                    self.current_level += 1
                    self.boss_killed = 0
                    if self.current_level in [2, 3]:
                        result = self.show_dialog(self.current_level)
                        if result == 'quit':
                            return 'quit'
                    self.load_level()
                elif result == 'start' and self.current_level == self.MAX_LEVEL:
                    self.game_state = 'final_victory'

    def _update_game(self):
        current_level_data = levels[self.current_level - 1]
        if self.level_start_time == 0:
            self.level_start_time = pygame.time.get_ticks()

        if not self.boss_manager.is_boss_active():
            if len(self.aliens) < current_level_data.aliens_count:
                self.alien_spawn_timer += 1
                if self.alien_spawn_timer >= self.alien_spawn_delay / 1000 * 60:
                    self.alien_spawn_timer = 0
                    if len(self.aliens) < current_level_data.aliens_count:
                        controls.create_aliens(self.screen, self.aliens, self.boss_manager)
                    self.alien_spawn_delay = random.randint(500, 1000)
            if self.current_level in [2, 3]:
                self.asteroid_spawn_timer += 1
                max_asteroids = 40 if self.current_level == 3 else 18
                if self.asteroid_spawn_timer >= self.asteroid_spawn_delay / 1000 * 60 and len(self.asteroids) < max_asteroids:
                    self.asteroid_spawn_timer = 0
                    controls.create_asteroids(self.screen, self.asteroids, self.boss_manager)
                    self.asteroid_spawn_delay = random.randint(2000, 3000)

        killed = controls.update_bullets(self.screen, self.stats, self.real_score, self.aliens, self.asteroids, self.bullets, self.boss_manager, starship=self.starship)
        self.aliens_killed += killed

        controls.update_aliens(self.starship, self.aliens, self.real_score, self.stats, self.screen, self.bullets, self.asteroids, self.boss_manager, aliens_per_level={i + 1: level.aliens_count for i, level in enumerate(levels)}, current_level=self.current_level, speed=self.alien_speed)
        controls.update_asteroids(self.starship, self.aliens, real_score=self.real_score, stats=self.stats, screen=self.screen, bullets=self.bullets, asteroids=self.asteroids, boss_manager=self.boss_manager, asteroids_per_level={i + 1: level.asteroids_count for i, level in enumerate(levels)}, current_level=self.current_level, speed=self.asteroid_speed)
        result = self.boss_manager.handle_boss(self.screen, self.stats, self.bullets, self.starship)
        if result == "DEFEATED":
            self.boss_killed += 1

        if self.boss_manager.boss and hasattr(self.boss_manager.boss, 'bullets') and self.boss_manager.boss.bullets:
            boss_bullets = Group(self.boss_manager.boss.bullets)
            collisions = pygame.sprite.spritecollide(self.starship, boss_bullets, True)
            if collisions:
                self.stats.starship_left = self.stats.starship_left - len(collisions) if self.stats.starship_left is not None else 0
                if self.stats.starship_left <= 0:
                    self.game_state = 'game_over'

        self._check_level_completion()

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

    def load_level(self):
        current_level_data = levels[self.current_level - 1]
        self.starship.reset_position()
        temp_boss_killed = self.boss_killed
        self.aliens_killed = 0
        self.boss_killed = 0
        self.level_start_time = pygame.time.get_ticks()
        self.stats.starship_left = self.stats.starship_limit if self.stats.starship_limit is not None else 2
        for _ in range(current_level_data.aliens_count):
            if len(self.aliens) < current_level_data.aliens_count:
                controls.create_aliens(self.screen, self.aliens, self.boss_manager)
        if self.current_level == 1:
            initial_asteroids = 5
        elif self.current_level == 2:
            initial_asteroids = 3
        elif self.current_level == 3:
            initial_asteroids = 5
        for _ in range(initial_asteroids):
            if len(self.asteroids) < initial_asteroids:
                controls.create_asteroids(self.screen, self.asteroids, self.boss_manager)
        if temp_boss_killed == 1:
            self.boss_killed = 1

    def _check_level_completion(self):
        current_level_data = levels[self.current_level - 1]
        elapsed_time = (pygame.time.get_ticks() - self.level_start_time) / 1000
        print(f"Level {self.current_level}: aliens_killed={self.aliens_killed}/{current_level_data.target_aliens}, boss_killed={self.boss_killed}/{current_level_data.target_boss}, time={elapsed_time}")
        if current_level_data.survival_time > 0:
            if elapsed_time >= current_level_data.survival_time and self.stats.starship_left > 0:
                self.game_state = 'victory'
        elif self.aliens_killed >= current_level_data.target_aliens and self.boss_killed >= current_level_data.target_boss:
            self.game_state = 'victory'

    def _victory_screen(self, prev_level, final_aliens_killed, final_boss_killed, prev_target_aliens, prev_target_boss):
        self.audio.stop_music()
        print("Playing menu music in victory screen")
        self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
        running = True
        print(f"Victory screen - prev_level: {prev_level}, final_aliens_killed: {final_aliens_killed}/{prev_target_aliens}, final_boss_killed: {final_boss_killed}/{prev_target_boss}, MAX_LEVEL: {self.MAX_LEVEL}")

        while running:
            self.menu.draw_background()
            title_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 64)
            title = title_font.render("Ты победил!", True, (0, 191, 255))
            swirl = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36).render("~", True, (0, 191, 255))
            self.screen.blit(title, (250 - title.get_width() // 2, 100))
            self.screen.blit(swirl, (250 + title.get_width() // 2 - 20, 120))

            menu_rect = self.menu._draw_button("В главное меню", 350, "back")
            if prev_level < self.MAX_LEVEL:
                next_level_rect = self.menu._draw_button("Следующий уровень", 450, "free")

            font_task = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36)
            if levels[prev_level - 1].survival_time > 0:
                elapsed_time = (pygame.time.get_ticks() - self.level_start_time) / 1000
                time_text = font_task.render(f"Время выживания: {int(elapsed_time)}/60", True, (255, 255, 255))
                self.screen.blit(time_text, (250 - time_text.get_width() // 2, 490))
            else:
                aliens_text = font_task.render(f"Пришельцы: {min(final_aliens_killed, prev_target_aliens)}/{prev_target_aliens}", True, (255, 255, 255))
                boss_text = font_task.render(f"Босс: {final_boss_killed}/{prev_target_boss}", True, (255, 255, 255))
                self.screen.blit(aliens_text, (250 - aliens_text.get_width() // 2, 490))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if menu_rect.collidepoint(mouse_pos):
                        return 'menu'
                    if prev_level < self.MAX_LEVEL and next_level_rect.collidepoint(mouse_pos):
                        return 'start'

        return None

    def _game_over(self):
        self.audio.stop_music()
        print("Playing menu music in game over screen")
        self.audio.play_music('menu') if self.music_enabled else self.audio.stop_music()
        running = True

        while running:
            self.menu.draw_background()
            font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 72)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (250 - game_over_text.get_width() // 2, 150))

            restart_rect = self.menu._draw_button("Заново", 350, "free")
            menu_rect = self.menu._draw_button("В главное меню", 450, "back")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        return 'restart'
                    if menu_rect.collidepoint(mouse_pos):
                        return 'menu'

        return None

if __name__ == "__main__":
    game = StoryGame(screen)
    result = game.run()
    pygame.quit()