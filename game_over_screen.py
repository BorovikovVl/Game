import pygame

class Game_over():
    """экран после проигрыша + рестарт"""
    def __init__(self, screen):
        self.screen = screen

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))

        """текст GAME OVER"""
        font = pygame.font.SysFont('Arial', 64)
        text = font.render("Game Over", True, (255, 0, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(text, text_rect)

        """рестарт по кнопке"""
        font = pygame.font.SysFont('Arial', 36)
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        return True
        return False