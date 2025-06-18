import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 1.0

    def load_music(self, path):
        pygame.mixer.music.load(path)

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)