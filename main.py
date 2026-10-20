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

        # Draw game
        gui.draw(game)

        if pygame.mouse.get_pressed()[0]: # pygame.mouse.get_pressed() gives (False,False,False) for leftmouse,middlemouse,rightmouse
            mouse_x,mouse_y = pygame.mouse.get_pos()
            col = mouse_x // gui.tile_size_w
            row = mouse_y // gui.tile_size_h

            piece = game.piece_at(row,col)
            
            if piece:
                piece_image = gui.get_image_of_piece(piece)
                
                


    pygame.quit()


if __name__ == "__main__":
    main()