import pygame
import numpy as np

WIDTH = 800
HEIGHT = 800

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
            images[piece] = pygame.transform.scale(image, (80, 80))

        return images

    def get_image_of_piece(self, piece):
        return self.images[piece.get_name()]

    def draw(self, game, drag_piece, drag_pos):
        self.draw_board()
        self.draw_pieces(game, drag_piece, drag_pos)

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

    def draw_pieces(self, game, drag_piece=None, drag_pos=None):
        # White pieces
        for location, piece in game.white_pieces.items():
            image = self.images[f"white_{piece.type}"]
            if piece is drag_piece: # skip dragged piece
                self.screen.blit(image, drag_pos)
                continue

            x = location[0] * 100 + 10
            y = location[1] * 100 + 10

            self.screen.blit(image, (x, y))

        # Black pieces
        for location, piece in game.black_pieces.items():
            image = self.images[f"black_{piece.type}"]
            if piece is drag_piece: # skip dragged piece
                self.screen.blit(image, drag_pos)
                continue

            x = location[0] * 100 + 10
            y = location[1] * 100 + 10

            self.screen.blit(image, (x, y))

    def pixel_to_tile(self, x, y):
        col = x // self.tile_size_w
        row = y // self.tile_size_h
        return (col, row)