import pygame
import numpy as np

WIDTH = 800
HEIGHT = 800

PIECE_MARGIN = 10

PROMOTION_CHOICES = ["queen", "rook", "bishop", "knight"]

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

        self.highlight_surface = pygame.Surface((self.tile_size_w, self.tile_size_h), pygame.SRCALPHA) # sprite to draw on available squares when pikcing up piece
        pygame.draw.circle(
            self.highlight_surface,
            (0, 0, 0, 70), # low transparancy
            (self.tile_size_w // 2, self.tile_size_h // 2),  
            self.tile_size_w // 6 # radius
        )

        self.dragged_piece = None
        self.drag_pos = None
        self.grab_offset = (0, 0)
        self.origin = None
        self.highlighted_squares = []

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
        if game.pawn_promoted:
            self.draw_promotion_menu(game.pawn_promoted,game.turn)
        self.draw_highlighted_squares()

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
        img_dragged_piece = None
        # White pieces
        for location, piece in game.white_pieces.items():
            image = self.images[f"white_{piece.type}"]
            if piece is self.dragged_piece: # skip dragged piece
                img_dragged_piece = image
                continue

            x = location[0] * 100 + PIECE_MARGIN
            y = location[1] * 100 + PIECE_MARGIN

            self.screen.blit(image, (x, y))
        

        # Black pieces
        for location, piece in game.black_pieces.items():
            image = self.images[f"black_{piece.type}"]
            if piece is self.dragged_piece: # skip dragged piece
                img_dragged_piece = image
                continue

            x = location[0] * 100 + PIECE_MARGIN
            y = location[1] * 100 + PIECE_MARGIN

            self.screen.blit(image, (x, y))

        if self.dragged_piece:
            self.screen.blit(img_dragged_piece, self.drag_pos) # Draw the dragged piece last so it hovers over the other piece's image instead of under

    def draw_highlighted_squares(self):
        for square in self.highlighted_squares:
            col, row = square.end
            x,y = col*self.tile_size_w,row*self.tile_size_h
            self.screen.blit(self.highlight_surface,(x,y))

    def start_drag(self, mouse_pos, piece, highlighted_squares):
        col, row = self.pixel_to_tile(*mouse_pos)
        mouse_x, mouse_y = mouse_pos
        self.dragged_piece = piece
        self.origin = (col, row)
        # Offset inside the tile so the piece doesn't jump to the cursor
        self.grab_offset = (
            mouse_x - (col * self.tile_size_w + PIECE_MARGIN),
            mouse_y - (row * self.tile_size_h + PIECE_MARGIN),
        )
        self.highlighted_squares = highlighted_squares
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
        self.highlighted_squares = []
        return result

    def pixel_to_tile(self, x, y):
        col = x // self.tile_size_w
        row = y // self.tile_size_h
        return (col, row)

    # Draws rectangles for promotion choice
    def promotion_rects(self, square):
        col, row = square
        direction = 1 if row == 0 else -1   # open toward the board's inside
        return [
            (PROMOTION_CHOICES[i],
            pygame.Rect(col * 100, (row + direction * i) * 100, 100, 100))
            for i in range(4)
        ]

    def draw_promotion_menu(self, square, color):  # color: "white" / "black"
        color = "black" if color else "white"
        for name, rect in self.promotion_rects(square):
            pygame.draw.rect(self.screen, "white", rect)
            pygame.draw.rect(self.screen, "black", rect, 2)  # border
            self.screen.blit(self.images[f"{color}_{name}"],
                            (rect.x + PIECE_MARGIN, rect.y + PIECE_MARGIN))

    def promotion_choice_at(self,pos,square):
        for name, rect in self.promotion_rects(square):
                if rect.collidepoint(pos):
                    return name
        return None