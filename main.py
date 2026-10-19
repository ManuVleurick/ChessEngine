import pygame

from game import Game
from gui import GUI


def main():
    game = Game()
    gui = GUI()

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game
        # game.update()

        # Draw game
        gui.draw(game)

    pygame.quit()


if __name__ == "__main__":
    main()