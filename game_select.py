import pygame
from start_menu import Menu
from Freemod_main import FreeModeGame
from Lvl_mod_main import StoryGame


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Starhip")

    clock = pygame.time.Clock()
    menu = Menu(screen)

    while True:
        # Главное меню
        result = menu.main_menu()

        if result == ('start', 'free'):
            game = FreeModeGame(screen)
            game.run()
        elif result == ('start', 'story'):
            game = StoryGame(screen)
            game.run()
        elif result == 'quit':
            pygame.quit()
            return

        clock.tick(260)


if __name__ == "__main__":
    main()