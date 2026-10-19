

class ChessPiece:
    def __init__(self,type):
        self.type = type
        self.has_moved = False

    def has_moved(self):
        return self.has_moved

    def is_type(self,type):
        return self.type == type
