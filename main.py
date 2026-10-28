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

            # Pick up
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game.pawn_promoted:

                col, row = gui.pixel_to_tile(*event.pos)
                piece = game.piece_at(col, row)
                if piece:
                    highlighted_squares = game.get_all_valid_moves((col,row))
                    gui.start_drag(event.pos, piece, highlighted_squares)

            # Move
            elif event.type == pygame.MOUSEMOTION:
                gui.update_drag(event.pos)

            # Drop
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if game.pawn_promoted:
                    choice = gui.promotion_choice_at(event.pos, game.pawn_promoted)
                    if choice:
                        game.promote(choice)
                else:
                    result = gui.end_drag(event.pos)
                    if result:
                        origin, target = result
                        if target != origin:
                            game.move_piece(origin, target) # Will check first then update game
                

        gui.draw(game)
                

    pygame.quit()


if __name__ == "__main__":
    main()