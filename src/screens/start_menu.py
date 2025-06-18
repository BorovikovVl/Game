import pygame
import random

class Menu:
    '''Инициализация меню в игре'''
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.stars = []  # Список координат звезд
        self.generate_stars()

        # Шрифты
        self.title_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 64)  # Ретро-шрифт с пикселями
        self.option_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36)

        # Цвета
        self.bg_color = (0, 0, 20)  # Темно-синий фон
        self.normal_color = (255, 255, 255)  # Белый текст
        self.hover_color = (150, 150, 130)  # Серый для наведения
        self.button_colors = {
            "start": (0, 170, 200),  # Зеленый (Start)
            "exit": (255, 0, 0),  # Красный (Exit)
            "free": (0, 170, 200),  # Зеленый для подменю
            "story": (77, 77, 77),  # Зеленый для подменю
            "settings": (77, 77, 77),  # Оранжевый (Settings)
            "back": (255, 0, 0),  # Красный (Back)
            "info": (77, 77, 255)  # Синий для "Свойства"
        }
        self.border_color = (100, 100, 120)  # Граница
        self.shadow_color = (0, 0, 0, 150)  # Темная тень для 3D
        self.bevel_light = (200, 200, 200)  # Светлый оттенок для скошенных краев
        self.bevel_dark = (50, 50, 50)  # Темный оттенок для скошенных краев
        self.title_color = (100, 14, 255)  # Сине-голубой для заголовка

        # Загрузка изображений
        self.alien_image = pygame.image.load('assets/image/alien.png')  # Изображение пришельца
        self.alien_image = pygame.transform.scale(self.alien_image, (40, 40))  # Масштабирование
        self.asteroid_image = pygame.image.load('assets/image/asteroid_3.png')  # Изображение астероида
        self.asteroid_image = pygame.transform.scale(self.asteroid_image, (40, 40))  # Масштабирование
        self.boss_image = pygame.image.load('assets/image/boss.png')  # Изображение босса
        self.boss_image = pygame.transform.scale(self.boss_image, (69, 57))  # Масштабирование (чуть больше)
        self.bonus_life_image = pygame.image.load('assets/image/new_red_heart.png')  # Доп. жизни
        self.bonus_life_image = pygame.transform.scale(self.bonus_life_image, (49, 49))  # Масштабирование
        self.bonus_fast_bullets_image = pygame.image.load('assets/image/bonus_fast_bullet.png')  # Быстрые пули
        self.bonus_fast_bullets_image = pygame.transform.scale(self.bonus_fast_bullets_image, (46, 46))  # Масштабирование
        self.bonus_shield_image = pygame.image.load('assets/image/shield (2).png')  # Щит
        self.bonus_shield_image = pygame.transform.scale(self.bonus_shield_image, (55, 45))  # Масштабирование

    def generate_stars(self):
        """Генерация звезд для фона"""
        self.stars = []
        for _ in range(100):  # Количество звезд
            x = random.randint(0, 600)
            y = random.randint(0, 800)
            size = random.randint(1, 3)
            self.stars.append((x, y, size))

    def draw_background(self):
        """Отрисовка фона с звездами и градиентом"""
        # Градиент от темно-синего к черному
        for y in range(800):
            r = int(0 + (y / 800) * 20)
            g = int(0 + (y / 800) * 20)
            b = int(20 + (y / 800) * 20)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (600, y))
        # Отрисовка звезд
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size)

    def main_menu(self):
        while True:
            self.draw_background()

            # Заголовок "Starship" с завитком
            title = self.title_font.render("Starship", True, self.title_color)
            swirl = self.option_font.render("", True, self.title_color)  # Символ завитка
            self.screen.blit(title, (300 - title.get_width() // 2, 100))
            self.screen.blit(swirl, (300 + title.get_width() // 2 - 20, 120))

            # Кнопки главного меню
            start_rect = self._draw_button("Start", 250, "start")  # Синяя
            info_rect = self._draw_button("Свойства", 320, "info")  # Синяя
            settings_rect = self._draw_button("Settings", 390, "settings")  # Черная
            exit_rect = self._draw_button("Exit", 460, "exit")  # Красная

            # Показатель счета
            score_text = self.option_font.render("Record: 26690", True, (255, 255, 255))
            self.screen.blit(score_text, (300 - score_text.get_width() // 2, 540))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        return self.mode_select_menu()  # Передаем управление подменю
                    if info_rect.collidepoint(mouse_pos):
                        return self.info_menu()  # Переход в подменю "Свойства"
                    if settings_rect.collidepoint(mouse_pos):
                        return 'settings'  # Возвращаем 'settings' для обработки
                    if exit_rect.collidepoint(mouse_pos):
                        return 'quit'

            pygame.display.flip()
            self.clock.tick(260)

    def info_menu(self):
        while True:
            self.draw_background()

            # Заголовок
            title_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 50)
            title = title_font.render("Свойства", True, (0, 191, 255))
            self.screen.blit(title, (300 - title.get_width() // 2, 50))

            # Информация
            font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)
            y_offset = 120

            # Управление
            controls_text = [
                "Управление:",
                "WASD - движение",
                "Backspace - стрельба",
                "Esc - пауза"
            ]
            for line in controls_text:
                text_surface = font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += 30

            y_offset += 20  # Отступ перед следующим разделом

            # Космические объекты
            objects_text = [
                ":",  # Пришельцы
                " - уничтожаются,дают очки",
                ":",  # Астероиды
                " - не уничтожаются",
                ":",  # Босс
                "  - босс"
            ]
            for i, line in enumerate(objects_text):
                if i == 0:  # Пришельцы
                    self.screen.blit(self.alien_image, (50, y_offset))
                elif i == 2:  # Астероиды
                    self.screen.blit(self.asteroid_image, (50, y_offset))
                elif i == 4:  # Босс
                    self.screen.blit(self.boss_image, (50, y_offset))
                else:
                    text_surface = font.render(line, True, (255, 255, 255))
                    self.screen.blit(text_surface, (90, y_offset))  # Смещение вправо для текста
                y_offset += 30

            y_offset += 20  # Отступ перед следующим разделом

            # Бонусы
            bonuses_text = [
                ":",  # Доп. жизни
                " - дополнительная жизнь",
                ":",  # Быстрые пули
                " - быстрая стрельба",
                ":",  # Щит
                " - защита от урона"
            ]
            for i, line in enumerate(bonuses_text):
                if i == 0:  # Доп. жизни
                    self.screen.blit(self.bonus_life_image, (50, y_offset))
                elif i == 2:  # Быстрые пули
                    self.screen.blit(self.bonus_fast_bullets_image, (50, y_offset))
                elif i == 4:  # Щит
                    self.screen.blit(self.bonus_shield_image, (50, y_offset))
                else:
                    text_surface = font.render(line, True, (255, 255, 255))
                    self.screen.blit(text_surface, (90, y_offset))  # Смещение вправо для текста
                y_offset += 30

            # Кнопка "Назад"
            back_rect = self._draw_button("Назад", 700, "back")

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        return None  # Возвращает в главное меню

            pygame.display.flip()
            self.clock.tick(260)

    def mode_select_menu(self):
        while True:
            self.draw_background()

            # Заголовок
            title = self.title_font.render("Select", True, self.title_color)
            self.screen.blit(title, (300 - title.get_width() // 2, 100))

            # Кнопки подменю с расстоянием между ними
            base_y = 270
            spacing = 100  # Расстояние между кнопками
            free_rect = self._draw_button("Free mode", base_y, "free")  # Зеленая
            story_rect = self._draw_button("Lvl mode", base_y + spacing, "story")  # Зеленая
            back_rect = self._draw_button("Exit", base_y + 2 * spacing, "back")  # Красная

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if free_rect.collidepoint(mouse_pos):
                        return ('start', 'free')
                    if story_rect.collidepoint(mouse_pos):
                        return ('start', 'story')
                    if back_rect.collidepoint(mouse_pos):
                        return None  # Возвращает в главное меню

            pygame.display.flip()
            self.clock.tick(260)

    def pause_menu(self, current_level=None):
        paused = True
        while paused:
            self.draw_background()
            # Наложение для паузы
            overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # Заголовок
            pause_text = self.title_font.render("ПАУЗА", True, (255, 255, 255))
            self.screen.blit(pause_text, (300 - pause_text.get_width() // 2, 300))

            # Кнопки
            continue_rect = self._draw_button("Продолжить (ESC)", 400, "free")  # Зеленая
            menu_rect = self._draw_button("В главное меню", 470, "back")  # Красная

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'continue'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_rect.collidepoint(mouse_pos):
                        return 'continue'
                    if menu_rect.collidepoint(mouse_pos):
                        return 'menu'

            pygame.display.flip()
            self.clock.tick(260)

    def settings_menu(self, audio, volume, music_enabled):
        running = True
        slider_rect = pygame.Rect(150, 300, 300, 20)
        slider_knob_x = 150 + int(volume * 300)
        knob_rect = pygame.Rect(slider_knob_x - 5, 295, 10, 30)
        self.dragging = False

        while running:
            self.draw_background()
            # Наложение для паузы/настроек
            overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # Заголовок
            title_text = self.title_font.render("Настройки", True, self.normal_color)
            self.screen.blit(title_text, (300 - title_text.get_width() // 2, 100))

            # Ползунок громкости
            pygame.draw.rect(self.screen, (100, 100, 100), slider_rect)  # Полоса ползунка
            pygame.draw.rect(self.screen, (0, 255, 0), knob_rect)  # Зеленый бегунок
            volume_text = self.option_font.render(f"Громкость: {int(volume * 100)}%", True, self.normal_color)
            self.screen.blit(volume_text, (300 - volume_text.get_width() // 2, 250))

            # Переключатель музыки
            music_text = self.option_font.render(f"Музыка: {'Вкл' if music_enabled else 'Выкл'}", True,
                                                 self.normal_color)
            music_rect = music_text.get_rect(center=(300, 400))
            self.screen.blit(music_text, music_rect)

            # Кнопка назад
            back_rect = self._draw_button("Назад", 500, "back")  # Красная

            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return volume, music_enabled, 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if knob_rect.collidepoint(mouse_pos):
                        self.dragging = True
                    elif slider_rect.collidepoint(mouse_pos):
                        volume = max(0, min(1.0, (mouse_pos[0] - 150) / 300))
                        audio.set_volume(volume)  # Применяем громкость сразу
                        if music_enabled and not pygame.mixer.music.get_busy():
                            audio.play_music('menu')  # Запускаем, если музыка выключена
                        elif music_enabled:
                            audio.stop_music()  # Останавливаем
                            audio.play_music('menu')  # Перезапускаем
                        slider_knob_x = 150 + int(volume * 300)
                        knob_rect = pygame.Rect(slider_knob_x - 5, 295, 10, 30)
                    if music_rect.collidepoint(mouse_pos):
                        music_enabled = not music_enabled
                        if music_enabled:
                            audio.play_music('menu')
                        else:
                            audio.stop_music()
                    if back_rect.collidepoint(mouse_pos):
                        running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                if event.type == pygame.MOUSEMOTION and self.dragging:
                    if slider_rect.collidepoint(mouse_pos):
                        volume = max(0, min(1.0, (mouse_pos[0] - 150) / 300))
                        audio.set_volume(volume)  # Применяем громкость сразу
                        if music_enabled and not pygame.mixer.music.get_busy():
                            audio.play_music('menu')  # Запускаем, если музыка выключена
                        elif music_enabled:
                            audio.stop_music()  # Останавливаем
                            audio.play_music('menu')  # Перезапускаем
                        slider_knob_x = 150 + int(volume * 300)
                        knob_rect = pygame.Rect(slider_knob_x - 5, 295, 10, 30)

            pygame.display.flip()
            self.clock.tick(260)

        return volume, music_enabled, 'back_to_menu'  # Изменено на 'back_to_menu' для возврата в mode_select_menu или main_menu

    def _draw_button(self, text, y, button_type):
        mouse_pos = pygame.mouse.get_pos()
        text_surf = self.option_font.render(text, True,
                                            self.hover_color if self._is_hover(y, text) else self.normal_color)
        text_rect = text_surf.get_rect(center=(300, y))

        # Увеличенная ширина для пиксельного стиля
        button_width = text_rect.width + 80  # Увеличена ширина
        button_height = text_rect.height + 20
        base_x = 300 - button_width // 2
        base_y = y - button_height // 2

        # Генерация неровных краев для пиксельного стиля
        points = [
            (base_x + random.randint(-5, 5), base_y + random.randint(-5, 5)),  # Верхний левый
            (base_x + button_width + random.randint(-5, 5), base_y + random.randint(-5, 5)),  # Верхний правый
            (base_x + button_width + random.randint(-5, 5), base_y + button_height + random.randint(-5, 5)),
            # Нижний правый
            (base_x + random.randint(-5, 5), base_y + button_height + random.randint(-5, 5))  # Нижний левый
        ]

        # Отрисовка тени для эффекта 3D
        shadow_points = [(x + 6, y + 6) for x, y in points]
        pygame.draw.polygon(self.screen, self.shadow_color, shadow_points)

        # Отрисовка скошенных краев
        bevel_points = [(x + 2, y + 2) for x, y in points]
        pygame.draw.polygon(self.screen, self.bevel_light,
                            [bevel_points[0], bevel_points[1], (bevel_points[1][0] - 2, bevel_points[1][1] + 2),
                             (bevel_points[0][0] - 2, bevel_points[0][1] + 2)])
        pygame.draw.polygon(self.screen, self.bevel_dark,
                            [bevel_points[2], bevel_points[3], (bevel_points[3][0] + 2, bevel_points[3][1] - 2),
                             (bevel_points[2][0] + 2, bevel_points[2][1] - 2)])

        # Отрисовка границы
        pygame.draw.polygon(self.screen, self.border_color, points, 4)

        # Отрисовка фона кнопки с градиентом
        inner_points = [(x + 6, y + 6) for x, y in points]
        inner_width = button_width - 12
        inner_height = button_height - 12
        base_color = self.button_colors[button_type]
        for i in range(4):
            gradient_points = [
                (inner_points[0][0] + i, inner_points[0][1] + i),
                (inner_points[1][0] - i, inner_points[1][1] + i),
                (inner_points[2][0] - i, inner_points[2][1] - i),
                (inner_points[3][0] + i, inner_points[3][1] - i)
            ]
            gradient_factor = 1.0 - (i * 0.2)  # Уменьшение яркости для градиента
            gradient_color = (int(base_color[0] * gradient_factor), int(base_color[1] * gradient_factor),
                              int(base_color[2] * gradient_factor))
            pygame.draw.polygon(self.screen, gradient_color, gradient_points)

        # Отрисовка текста
        self.screen.blit(text_surf, text_rect)
        return pygame.Rect(base_x, base_y, button_width, button_height)

    def _is_hover(self, y, text):
        text_surf = self.option_font.render(text, True, self.normal_color)
        text_rect = text_surf.get_rect(center=(300, y))
        button_width = text_rect.width + 80  # Увеличенная ширина
        button_height = text_rect.height + 20
        button_rect = pygame.Rect(300 - button_width // 2, y - button_height // 2, button_width, button_height)
        return button_rect.collidepoint(pygame.mouse.get_pos())