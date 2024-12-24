from Piece import Piece
class Bishop(Piece):
    def possibleMoves(self) -> list:
        return None

    def move(self, newpos) -> bool:
        self.pos = newpos

    def __str__(self):
        return 'B'