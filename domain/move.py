

class Move:

    def __init__(self,piece,start,end):
        self.piece = piece
        self.start = start
        self.end = end

    def is_valid(self):
        match self.piece:
            case "pawn":
                return self.valid_pawn_move()
            case "rook":
                return self.valid_rook_move()
            case "bishop":
                return self.valid_bishop_move()
            case "knight":
                return self.valid_knight_move()
            case "queen":
                return self.valid_queen_move()
            case "king":
                return self.valid_king_move()
            case _:
                raise Exception(f"Chess piece {self.piece} unknown")

    def valid_king_move(self):
        pass
            