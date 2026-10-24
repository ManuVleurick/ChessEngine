import pygame
import numpy as np

WIDTH = 800
HEIGHT = 800

PIECE_MARGIN = 10

class GUI:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")

        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.medium_font = pygame.font.Font("freesansbold.ttf", 40)
        self.big_font = pygame.font.Font("freesansbold.ttf", 60)

        self.images = self.load_images()

        self.tile_size_w = WIDTH // 8
        self.tile_size_h = HEIGHT // 8

        self.dragged_piece = None
        self.drag_pos = None
        self.grab_offset = (0, 0)
        self.origin = None

    def load_images(self):
        images = {}

        pieces = [
            "black_queen",
            "black_king",
            "black_rook",
            "black_bishop",
            "black_knight",
            "black_pawn",
            "white_queen",
            "white_king",
            "white_rook",
            "white_bishop",
            "white_knight",
            "white_pawn"
        ]

        for piece in pieces:
            image = pygame.image.load(f"images/{piece}.png")
            images[piece] = pygame.transform.scale(image, (WIDTH/10, HEIGHT/10))

        return images

    def get_image_of_piece(self, piece):
        return self.images[piece.get_name()]

    def draw(self, game):
        self.draw_board()
        self.draw_pieces(game)

        pygame.display.flip()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = "light gray" if (row + col) % 2 == 0 else "gray"

                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * 100, row * 100, 100, 100)
                )

    def draw_pieces(self, game):
        # White pieces
        for location, piece in game.white_pieces.items():
            image = self.images[f"white_{piece.type}"]
            if piece is self.dragged_piece: # skip dragged piece
                self.screen.blit(image, self.drag_pos)
                continue

            x = location[0] * 100 + PIECE_MARGIN
            y = location[1] * 100 + PIECE_MARGIN

            self.screen.blit(image, (x, y))

        # Black pieces
        for location, piece in game.black_pieces.items():
            image = self.images[f"black_{piece.type}"]
            if piece is self.dragged_piece: # skip dragged piece
                self.screen.blit(image, self.drag_pos)
                continue

            x = location[0] * 100 + PIECE_MARGIN
            y = location[1] * 100 + PIECE_MARGIN

            self.screen.blit(image, (x, y))

    def start_drag(self, mouse_pos, piece):
        col, row = self.pixel_to_tile(*mouse_pos)
        mouse_x, mouse_y = mouse_pos
        self.dragged_piece = piece
        self.origin = (col, row)
        # Offset inside the tile so the piece doesn't jump to the cursor
        self.grab_offset = (
            mouse_x - (col * self.tile_size_w + PIECE_MARGIN),
            mouse_y - (row * self.tile_size_h + PIECE_MARGIN),
        )
        self.update_drag(mouse_pos) # Update drag_pos

    def update_drag(self,mouse_pos):
        if self.dragged_piece:
            self.drag_pos = (
                mouse_pos[0] - self.grab_offset[0],
                mouse_pos[1] - self.grab_offset[1],
            )

    def end_drag(self,mouse_pos):
        if not self.dragged_piece:
            return None
        result = (self.origin, self.pixel_to_tile(*mouse_pos))
        self.dragged_piece = None
        self.drag_pos = None
        self.origin = None
        return result

    def pixel_to_tile(self, x, y):
        col = x // self.tile_size_w
        row = y // self.tile_size_h
        return (col, row)