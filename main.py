import pygame

from game import Game
from gui import GUI


def main():
    game = Game()
    gui = GUI()

    clock = pygame.time.Clock()

    running = True
    dragged_piece = None
    drag_pos = None
    grab_offset = (0,0)
    origin = None

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pick up
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                col, row = gui.pixel_to_tile(mouse_x, mouse_y)
                piece = game.piece_at(col, row)

                if piece:
                    dragged_piece = piece
                    origin = (col, row)
                    # Offset inside the tile so the piece doesn't jump to the cursor
                    grab_offset = (
                        mouse_x - col * gui.tile_size_w,
                        mouse_y - row * gui.tile_size_h,
                    )
                    drag_pos = (mouse_x - grab_offset[0], mouse_y - grab_offset[1])

            # Move
            elif event.type == pygame.MOUSEMOTION and dragged_piece:
                mouse_x, mouse_y = event.pos
                drag_pos = (mouse_x - grab_offset[0], mouse_y - grab_offset[1])

            # Drop
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragged_piece:
                col, row = gui.pixel_to_tile(*event.pos)
                
                if (col, row) != origin: # not dragged back to starting square.
                    game.move_piece(origin, (col, row)) # will check and if True update game

                dragged_piece = None
                drag_pos = None
                origin = None

        gui.draw(game, dragged_piece, drag_pos)
                

    pygame.quit()


if __name__ == "__main__":
    main()