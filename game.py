from domain.chesspiece import ChessPiece

class Game:
    def __init__(self):
        self.white_pieces = [
            ChessPiece('rook'), ChessPiece('knight'), ChessPiece('bishop'), ChessPiece('king'),
            ChessPiece('queen'), ChessPiece('bishop'), ChessPiece('knight'), ChessPiece('rook'),
            ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'),
            ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn')
        ]

        self.black_locations = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (4, 0), (5, 0), (6, 0), (7, 0),
            (0, 1), (1, 1), (2, 1), (3, 1),
            (4, 1), (5, 1), (6, 1), (7, 1)
        ]

        self.black_pieces = [
            ChessPiece('rook'), ChessPiece('knight'), ChessPiece('bishop'), ChessPiece('king'),
            ChessPiece('queen'), ChessPiece('bishop'), ChessPiece('knight'), ChessPiece('rook'),
            ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'),
            ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn'), ChessPiece('pawn')
        ]

        self.white_locations = [
            (0, 7), (1, 7), (2, 7), (3, 7),
            (4, 7), (5, 7), (6, 7), (7, 7),
            (0, 6), (1, 6), (2, 6), (3, 6),
            (4, 6), (5, 6), (6, 6), (7, 6)
        ]

        self.board = 0xFFFF00000000FFFF # square h1 represents 0x0000000000000001, one hexdecimal is 4 bits
        #8  a8 b8 c8 d8 e8 f8 g8 h8
        #7  a7 b7 c7 d7 e7 f7 g7 h7
        #6  a6 b6 c6 d6 e6 f6 g6 h6
        #5  a5 b5 c5 d5 e5 f5 g5 h5
        #4  a4 b4 c4 d4 e4 f4 g4 h4
        #3  a3 b3 c3 d3 e3 f3 g3 h3
        #2  a2 b2 c2 d2 e2 f2 g2 h2
        #1  a1 b1 c1 d1 e1 f1 g1 h1

        self.turn = 0 # 0 is white and 1 is black
        self.selected_piece = None

    def move(self, piece, start, end):
        pass

    def is_white_turn(self):
        return self.turn == 0

    def update_board(self,start,end,is_castling):
        if is_castling:
            
        
