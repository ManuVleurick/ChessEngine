

class ChessPiece:
    def __init__(self,type, color):
        self.type = type
        self.color = color # 0 for white 1 for black
        self.has_moved = False # For rooks, should be false for king to castle

    def has_moved(self):
        return self.has_moved

    def is_type(self,type):
        return self.type == type

    def get_name(self):
        if self.color:
            return f"black_{self.type}"
        return f"white_{self.type}"
