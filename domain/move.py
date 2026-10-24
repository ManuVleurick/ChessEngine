

class Move:

    def __init__(self, piece, start, end, boards, pieces, turn):
        self.piece = piece
        self.start = start # type of (col,row)[(Int,Int)]
        self.end = end
        self.white_board = boards[0]
        self.black_board = boards[1]
        self.white_pieces = pieces[0]
        self.black_pieces = pieces[1]
        self.turn = turn

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

    def valid_pawn_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end
        # check if moving one square forward, two squares forward or diagonally
        if self.turn:
            if start_col != end_col: # diagonally
                return self.is_piece_at(turn=1) # check if it can capture a piece there
            elif start_row + 1 == end_row: # one square forward
                return not self.is_piece_at(turn=1) # check if there is no piece there
            elif start_row + 2 == end_row and not self.piece.has_moved: # two square forward
                self.piece.has_moved = True
                return not (self.is_piece_at(square=(start_col,start_row+1), turn=1) or self.is_piece_at(turn=1))
        else:
            if start_col != end_col: # diagonally
                return self.is_piece_at(turn=0)
            elif start_row - 1 == end_row: # one square forward
                return not self.is_piece_at(turn=0)
            elif start_row - 2 == end_row and not self.piece_has_moved: # two square forward
                self.piece.has_moved = True
                return not (self.is_piece_at(square=(start_col,start_row-1), turn=0) or self.is_piece_at(turn=0))
        
        # check for promotion too

        return False