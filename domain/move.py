

class Move:

    def __init__(self, piece, start, end, boards, pieces, en_passant_target, turn):
        self.piece = piece
        self.start = start # type of (col,row)[(Int,Int)]
        self.end = end
        white_board = boards[0]
        black_board = boards[1]
        self.turn = turn
        self.own_board, self.enemy_board = (black_board,white_board) if turn else (white_board,black_board)
        white_pieces = pieces[0]
        black_pieces = pieces[1]
        self.own_pieces, self.enemy_pieces = (black_pieces, white_pieces) if turn else (white_pieces, black_pieces)

        self.en_passant_target = en_passant_target

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
            # Globally when piece has moved, check if king is in check then not valid move

    def valid_pawn_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end

        if not self.in_board(self.end): return False # Move goes outside board

        dir = 1 if self.turn == 1 else -1
        # check if moving one square forward, two squares forward or diagonally
        if (start_row + dir == end_row and (start_col + 1 == end_col or start_col - 1 == end_col)): # diagonally, needs to have enemy
            return self.has_enemy(self.end) or (self.en_passant_target == self.end) # check if it can capture a piece there or en passant
        elif (start_row + dir == end_row and start_col == end_col): # one square forward
            return self.is_empty(self.end) # check if there is no piece there
        elif start_row + 2*dir == end_row and start_col == end_col and not self.piece.has_moved: # two square forward
            if (self.is_empty((start_col, start_row+dir)) and self.is_empty(self.end)):
                return True

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

        return True


    def valid_knight_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end
        # Check 8 position if not has_own and in_board
        if not self.in_board(self.end): return False # Move goes outside board

        if abs(end_col - start_col) == 2 and abs(end_row - start_row) == 1:
            return not self.has_own(self.end)
        elif abs(end_col - start_col) == 1 and abs(end_row - start_row) == 2:
            return not self.has_own(self.end)

        return False

    def valid_queen_move(self):
        return self.valid_bishop_move() or self.valid_rook_move()

    def valid_king_move(self):
        start_col, start_row = self.start
        end_col, end_row = self.end

        if not self.in_board(self.end): return False # Move goes outside board

        if abs(end_col - start_col) <= 1 and abs(end_row - start_row) <= 1:
            return not self.has_own(self.end)
        
        # castling
        if abs(end_col - start_col) == 2 and not self.piece.has_moved and start_col == 4:
            king_row = 0 if self.turn else 7
            if not king_row == start_row or self.is_square_attacked(self.start): # check if king is on starting row and is not in check
                return False
            dir = 1 if (end_col - start_col > 0) else -1 # 1 is king side and -1 queen side
            if dir == 1:
                rook_moved = self.own_pieces[(0,0)].has_moved if self.turn else self.own_pieces[(7,7)].has_moved
                # empty squares between king and rook checked if empty and not attacked
                if not rook_moved:
                    col = start_col + dir
                    while (col, start_row) != (end_col, end_row):  # stop before the end square
                        if not self.is_empty((col, start_row)) and not self.is_square_attacked((col,start_row)):
                            return False
                        col += dir
            else:
                rook_moved = self.own_pieces[(7,0)].has_moved if self.turn else self.own_pieces[(0,7)].has_moved
                if not rook_moved:
                    col = start_col + dir
                    while (col, start_row) != (end_col+1, end_row):  # stop before the end square
                        if not self.is_empty((col, start_row)) and not self.is_square_attacked((col,start_row)):
                            return False
                        col += dir
                


        return False

    def is_square_attacked(self, square):
        pass


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