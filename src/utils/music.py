import pygame.mixer

class AudioManager:
    def __init__(self):
        pygame.mixer.init()  # Инициализация микшера
        self.music_files = {}  # Словарь для хранения путей к файлам музыки

    def load_music(self, music_type, file_path):
        """Загружает музыкальный файл для указанного типа."""
        if music_type not in ['menu', 'game', 'click']:
            raise ValueError("Invalid music type. Use 'menu', 'game', or 'click'.")
        self.music_files[music_type] = file_path
        if music_type in ['menu', 'game']:  # Загружаем в mixer только для фоновой музыки
            pygame.mixer.music.load(file_path)

    def play_music(self, music_type):
        """Воспроизводит музыку указанного типа."""
        if music_type not in self.music_files:
            raise ValueError(f"No music loaded for type '{music_type}'.")
        if music_type in ['menu', 'game']:
            pygame.mixer.music.load(self.music_files[music_type])  # Перезагружаем для переключения
            pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
        elif music_type == 'click':
            sound = pygame.mixer.Sound(self.music_files[music_type])
            sound.play()

    def stop_music(self):
        """Останавливает воспроизведение музыки."""
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        """Устанавливает громкость (0.0 to 1.0)."""
        pygame.mixer.music.set_volume(volume)