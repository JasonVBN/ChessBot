from Piece import Piece
class Pawn(Piece):
    def possibleMoves(self) -> list:
        r,c=self.pos
        ans = []
        if self.color=='w':
            ans.append((r-1,c))
            if self.pos[0]==6:
                ans.append((r-2,c))
        if self.color=='b':
            ans.append((r+1,c))
            if self.pos[0] == 1:
                ans.append((r+2, c))
        return ans

    def move(self, newpos) -> bool:
        self.pos = newpos

    def __str__(self):
        return 'P'