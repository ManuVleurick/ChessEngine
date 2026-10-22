import numpy as np

from domain.chesspiece import ChessPiece

class Game:
    def __init__(self):

        self.white_pieces = dict({
            (0, 0) : ChessPiece('rook', 0),
            (1, 0) : ChessPiece('knight', 0),
            (2, 0) : ChessPiece('bishop', 0), 
            (3, 0) : ChessPiece('king', 0),
            (4, 0) : ChessPiece('queen', 0), 
            (5, 0) : ChessPiece('bishop', 0), 
            (6, 0) : ChessPiece('knight', 0), 
            (7, 0) : ChessPiece('rook', 0),
            (0, 1) : ChessPiece('pawn', 0), 
            (1, 1) : ChessPiece('pawn', 0), 
            (2, 1) : ChessPiece('pawn', 0), 
            (3, 1) : ChessPiece('pawn', 0),
            (4, 1) : ChessPiece('pawn', 0), 
            (5, 1) : ChessPiece('pawn', 0), 
            (6, 1) : ChessPiece('pawn', 0), 
            (7, 1) : ChessPiece('pawn', 0)
        })

        self.black_pieces = dict({
            (0, 7) : ChessPiece('rook', 1), 
            (1, 7) : ChessPiece('knight', 1), 
            (2, 7) : ChessPiece('bishop', 1), 
            (3, 7) : ChessPiece('king', 1),
            (4, 7) : ChessPiece('queen', 1), 
            (5, 7) : ChessPiece('bishop', 1), 
            (6, 7) : ChessPiece('knight', 1), 
            (7, 7) : ChessPiece('rook', 1),
            (0, 6) : ChessPiece('pawn', 1), 
            (1, 6) : ChessPiece('pawn', 1), 
            (2, 6) : ChessPiece('pawn', 1),
            (3, 6) : ChessPiece('pawn', 1),
            (4, 6) : ChessPiece('pawn', 1), 
            (5, 6) : ChessPiece('pawn', 1), 
            (6, 6) : ChessPiece('pawn', 1), 
            (7, 6) : ChessPiece('pawn', 1)
        })

        self.board = 0xFFFF00000000FFFF # square h1 represents 0x0000000000000001, one hexdecimal is 4 bits
        #8  a8 b8 c8 d8 e8 f8 g8 h8
        #7  a7 b7 c7 d7 e7 f7 g7 h7
        #6  a6 b6 c6 d6 e6 f6 g6 h6
        #5  a5 b5 c5 d5 e5 f5 g5 h5
        #4  a4 b4 c4 d4 e4 f4 g4 h4
        #3  a3 b3 c3 d3 e3 f3 g3 h3
        #2  a2 b2 c2 d2 e2 f2 g2 h2
        #1  a1 b1 c1 d1 e1 f1 g1 h1

        self.turn = False # False is white and True is black

    # Return domain Piece at row and col in board else None 
    def piece_at(self, col, row):
        if self.turn == 0:
            return self.white_pieces.get((col,row))
        else:
            return self.black_pieces.get((col,row))

    def update_bitboard(self,start,end):
        pass

    def is_valid_move(self, start, end):
        return True

    def move_piece(self, start, end):        
        if self.is_valid_move(start, end):
            # update dicts and bitboard
            if self.turn: # Black's turn
                self.black_pieces[end] = self.black_pieces.pop(start) # update dict
            else: # White's turn
                print(start)
                self.white_pieces[end] = self.white_pieces.pop(start) 

            self.update_bitboard(start, end)

            self.turn = not self.turn # other player turn
        
