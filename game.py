import numpy as np

from domain.chesspiece import ChessPiece
from domain.move import Move

class Game:
    def __init__(self):

        self.black_pieces = dict({
            (0, 0) : ChessPiece('rook', 1),
            (1, 0) : ChessPiece('knight', 1),
            (2, 0) : ChessPiece('bishop', 1), 
            (3, 0) : ChessPiece('queen', 1),
            (4, 0) : ChessPiece('king', 1), 
            (5, 0) : ChessPiece('bishop', 1), 
            (6, 0) : ChessPiece('knight', 1), 
            (7, 0) : ChessPiece('rook', 1),
            (0, 1) : ChessPiece('pawn', 1), 
            (1, 1) : ChessPiece('pawn', 1), 
            (2, 1) : ChessPiece('pawn', 1), 
            (3, 1) : ChessPiece('pawn', 1),
            (4, 1) : ChessPiece('pawn', 1), 
            (5, 1) : ChessPiece('pawn', 1), 
            (6, 1) : ChessPiece('pawn', 1), 
            (7, 1) : ChessPiece('pawn', 1)
        })

        self.white_pieces = dict({
            (0, 7) : ChessPiece('rook', 0), 
            (1, 7) : ChessPiece('knight', 0), 
            (2, 7) : ChessPiece('bishop', 0), 
            (3, 7) : ChessPiece('queen', 0),
            (4, 7) : ChessPiece('king', 0), 
            (5, 7) : ChessPiece('bishop', 0), 
            (6, 7) : ChessPiece('knight', 0), 
            (7, 7) : ChessPiece('rook', 0),
            (0, 6) : ChessPiece('pawn', 0), 
            (1, 6) : ChessPiece('pawn', 0), 
            (2, 6) : ChessPiece('pawn', 0),
            (3, 6) : ChessPiece('pawn', 0),
            (4, 6) : ChessPiece('pawn', 0), 
            (5, 6) : ChessPiece('pawn', 0), 
            (6, 6) : ChessPiece('pawn', 0), 
            (7, 6) : ChessPiece('pawn', 0)
        })

        self.white_board = 0xFFFF000000000000 # square h1 represents 0x0000000000000001, one hexdecimal is 4 bits
        self.black_board = 0x000000000000FFFF
        #8  a8 b8 c8 d8 e8 f8 g8 h8
        #7  a7 b7 c7 d7 e7 f7 g7 h7
        #6  a6 b6 c6 d6 e6 f6 g6 h6
        #5  a5 b5 c5 d5 e5 f5 g5 h5
        #4  a4 b4 c4 d4 e4 f4 g4 h4
        #3  a3 b3 c3 d3 e3 f3 g3 h3
        #2  a2 b2 c2 d2 e2 f2 g2 h2
        #1  a1 b1 c1 d1 e1 f1 g1 h1

        self.pawn_promoted = None
        self.en_passant_target = None

        self.turn = False # False is white and True is black

    # Return domain Piece at row and col in board else None 
    def piece_at(self, col, row):
        if not self.turn:
            return self.white_pieces.get((col,row))
        else:
            return self.black_pieces.get((col,row))

    def update_bitboard(self,start,end):
        start_col, start_row = start
        end_col, end_row = end
        start_square = start_row * 8 + start_col # convert coordinates to int 0-63 to convert to bits
        end_square = end_row * 8 + end_col
        start_mask = 1 << start_square # 0-63 bits where only at start_square is 1.
        end_mask = 1 << end_square
        if self.turn:
            self.black_board = (self.black_board & ~start_mask) | end_mask # Uses AND to remove starting loc. Uses OR to add end loc. ~ inverts  mask
            self.white_board = (self.white_board & ~end_mask) # in case of capture, remove piece from other player
        else:
            self.white_board = (self.white_board & ~start_mask) | end_mask
            self.black_board = (self.black_board & ~end_mask)

    # remove a bit from bitboard. Used for en passant
    def remove_square_bitboard(self, square):
        col, row = square
        square = row * 8 + col
        mask = 1 << square
        if self.turn:
            self.white_board = (self.white_board & ~mask)
        else:
            self.black_board = (self.black_board & ~mask)

    def is_valid_move(self, start, end):
        piece = self.piece_at(*start)
        if piece:
            move = Move(piece,start,end, (self.white_board,self.black_board), (self.white_pieces,self.black_pieces), self.en_passant_target, self.turn)
            return move.is_valid() and not move.king_under_attack()

    def move_piece(self, start, end):
        if self.pawn_promoted: return # pawn has to promote first 

        if self.is_valid_move(start, end):
            piece = self.piece_at(*start)
            last_row = 7 if self.turn else 0

            own_pieces = self.black_pieces if self.turn else self.white_pieces
            enemy_pieces = self.white_pieces if self.turn else self.black_pieces

            # update dicts and bitboard
            own_pieces[end] = own_pieces.pop(start) # update dict
            if piece.type == "pawn" and self.en_passant_target == end: # en passant was used
                dir = -1 if self.turn else 1
                enemy_pieces.pop((end[0],end[1]+dir), False)
                self.remove_square_bitboard((end[0],end[1]+dir))
            else:
                enemy_pieces.pop(end, False) # piece is captured and removed

            self.update_bitboard(start, end)

            # pawn promotion detected
            if piece.type == "pawn" and end[1] == last_row:
                self.pawn_promoted = end
                return  # don't switch turns yet

            self.en_passant_target = None # reset since en passant only available for one move
            # En passant is possible
            if piece.type == "pawn" and abs(end[1] - start[1]) == 2:
                dir = 1 if self.turn else -1
                self.en_passant_target = (start[0],start[1]+dir) # square between end and start is targetable

            # detect castling
            is_castling = piece.type == "king" and abs(end[0] - start[0]) == 2
            if is_castling:
                dir = 1 if end[0] > start[0] else -1
                rook_start_col = 7 if dir == 1 else 0
                rook_start_row = start[1]
                rook_end_col = (start[0] + end[0]) // 2

                own_pieces[(rook_end_col,rook_start_row)] = own_pieces.pop((rook_start_col,rook_start_row))
                self.update_bitboard((rook_start_col,rook_start_row),(rook_end_col,rook_start_row))

                rook = own_pieces.get((rook_end_col,rook_start_row))
                rook.has_moved = True

            piece.has_moved = True
            self.turn = not self.turn # other player turn
            self.print_debug()

    def promote(self, choice):  # "queen", "rook", "bishop" or "knight"
        pieces = self.black_pieces if self.turn else self.white_pieces
        pieces[self.pawn_promoted] = ChessPiece(choice, self.turn)
        self.pawn_promoted = None
        self.turn = not self.turn # next player
        self.print_debug()


    def get_all_valid_moves(self, start):
        moves = []
        piece = self.piece_at(*start)
        for row in range(8):
            for col in range(8):
                move = Move(piece,start,(col,row),(self.white_board,self.black_board), (self.white_pieces,self.black_pieces), self.en_passant_target, self.turn)
                if move.is_valid() and not move.king_under_attack():
                    moves.append(move)
        return moves

    # Debug    
    def bitboard_to_matrix(self, board):
        """8x8 list of 0/1; matrix[row][col], row 0 is the top (black's back rank)."""
        return [[(board >> (row * 8 + col)) & 1 for col in range(8)]
            for row in range(8)]

    def combined_bitboard_matrix(self):
        """8x8 matrix: W = white bit, B = black bit, . = empty, ! = both (a bug)."""
        white = self.bitboard_to_matrix(self.white_board)
        black = self.bitboard_to_matrix(self.black_board)
        return [["!" if white[r][c] and black[r][c]
                 else "W" if white[r][c]
                 else "B" if black[r][c]
                 else "." for c in range(8)]
                for r in range(8)]

    def piece_matrix(self):
        """8x8 matrix of piece letters: uppercase = white, lowercase = black."""
        letters = {"pawn": "p", "knight": "n", "bishop": "b",
                   "rook": "r", "queen": "q", "king": "k"}
        matrix = [["." for _ in range(8)] for _ in range(8)]
        for (col, row), piece in self.white_pieces.items():
            matrix[row][col] = letters[piece.type].upper()
        for (col, row), piece in self.black_pieces.items():
            # '!' marks a square present in both dicts, which should never happen
            matrix[row][col] = "!" if matrix[row][col] != "." else letters[piece.type]
        return matrix

    def print_debug(self):
        bits = self.combined_bitboard_matrix()
        pieces = self.piece_matrix()
        files = "a b c d e f g h"
        print(f"  {files}     {files}")
        print(f"{'BITBOARD':<18}{'PIECES'}")
        for row in range(8):
            rank = 8 - row
            print(f"{rank} {' '.join(bits[row])}   {rank} {' '.join(pieces[row])}")

        # consistency check: the bitboard and the piece dicts must agree on every square
        for r in range(8):
            for c in range(8):
                bit, piece = bits[r][c], pieces[r][c]
                expected = "." if piece == "." else ("W" if piece.isupper() else "B")
                if piece == "!" or bit == "!" or bit != expected:
                    print(f"MISMATCH at {'abcdefgh'[c]}{8 - r}")