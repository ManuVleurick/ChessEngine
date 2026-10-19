import pygame

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
        for piece, location in zip(
            game.white_pieces,
            game.white_locations
        ):
            image = self.images[f"white_{piece}"]

            x = location[0] * 100 + 10
            y = location[1] * 100 + 10

            self.screen.blit(image, (x, y))

        # Black pieces
        for piece, location in zip(
            game.black_pieces,
            game.black_locations
        ):
            image = self.images[f"black_{piece}"]

            x = location[0] * 100 + 10
            y = location[1] * 100 + 10

            self.screen.blit(image, (x, y))