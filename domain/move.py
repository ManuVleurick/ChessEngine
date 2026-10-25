

class Move:

    def __init__(self, piece, start, end, boards, pieces, turn):
        self.piece = piece
        self.start = start # type of (col,row)[(Int,Int)]
        self.end = end
        white_board = boards[0]
        black_board = boards[1]
        self.turn = turn
        self.own_board, self.enemy_board = (black_board,white_board) if turn else (white_board,black_board)
        self.white_pieces = pieces[0]
        self.black_pieces = pieces[1]

    def is_valid(self):
        match self.piece.type:
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

        if not self.in_board(self.end): return False # Move goes outside board

        dir = 1 if self.turn == 1 else -1
        # check if moving one square forward, two squares forward or diagonally
        if (start_row + dir == end_row and (start_col + 1 == end_col or start_col - 1 == end_col)): # diagonally, needs to have enemy
            self.piece.has_moved = True
            return self.has_enemy(self.end) # check if it can capture a piece there
        elif (start_row + dir == end_row and start_col == end_col): # one square forward
            self.piece.has_moved = True
            return self.is_empty(self.end) # check if there is no piece there
        elif start_row + 2*dir == end_row and start_col == end_col and not self.piece.has_moved: # two square forward
            if (self.is_empty((start_col, start_row+dir)) and self.is_empty(self.end)):
                self.piece.has_moved = True
                return True
        
        # TODO do promotion outside the Move class

        return False

    def valid_rook_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end

        if not self.in_board(self.end): return False # Move goes outside board
        if (self.start==self.end): return False # same square
        if self.has_own(self.end): return False # End square has own piece
        if start_col != end_col and start_row != end_row: return False  # not a straight line

        dc = (end_col > start_col) - (end_col < start_col)     # -1, 0 or 1
        dr = (end_row > start_row) - (end_row < start_row)
        col, row = start_col + dc, start_row + dr    # start one square past the rook
        while (col, row) != (end_col, end_row):  # stop before the end square
            if not self.is_empty((col, row)):
                return False
            col += dc
            row += dr

        self.piece.has_moved = True       
        return True

    def valid_bishop_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end

        if not self.in_board(self.end): return False # Move goes outside board
        if (self.start==self.end): return False # same square
        if self.has_own(self.end): return False # End square has own piece

        # check diagonal line
        if not abs(end_col - start_col) == abs(end_row - start_row):
            return False

        # check not blocked
        dir_col = 1 if (end_col - start_col > 0) else -1
        dir_row = 1 if (end_row - start_row > 0) else -1
        col, row = start_col + dir_col, start_row + dir_row
        while not (col, row) == (end_col, end_row):
            if not self.is_empty((col,row)):
                return False
            col, row = col + dir_col, row + dir_row

        self.piece.has_moved = True
        return True


    def valid_knight_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end
        # Check 8 position if not has_own and in_board
        if not self.in_board(self.end): return False # Move goes outside boardZ

        if abs(end_col - start_col) == 2 and abs(end_row - start_row) == 1:
            return not self.has_own(self.end)
        elif abs(end_col - start_col) == 1 and abs(end_row - start_row) == 2:
            return not self.has_own(self.end)

        return False

    def valid_queen_move(self):
        return self.valid_bishop_move() or self.valid_rook_move()

    def valid_king_move(self):
        return True

    def square_mask(self, square):
        col, row = square
        return 1 << (row*8 + col)

    def is_empty(self, square):
        return not ((self.own_board | self.enemy_board) & self.square_mask(square))

    def has_enemy(self, square):
        return bool(self.enemy_board & self.square_mask(square))

    def has_own(self, square):
        return bool(self.own_board & self.square_mask(square))

    def in_board(self,square):
        col, row = square
        return (col >= 0 and col < 8) and (row >= 0 and row < 8)