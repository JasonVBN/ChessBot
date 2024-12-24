import numpy as np
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen
from King import King

class Board:
    def __init__(self):
        self.grid = np.array([[None for c in range(8)] for r in range(8)])
        for row,color in [(0,'b'),(7,'w')]:
            self.grid[row,0] = Rook((row,0), color)
            self.grid[row,1] = Knight((row,1), color)
            self.grid[row,2] = Bishop((row,2), color)
            # this is so f---ing tedious
            self.grid[row,3] = Queen((row,3), color)
            self.grid[row,4] = King((row,4), color)
            self.grid[row,5] = Bishop((row,5), color)
            # why didn't we just use strings...
            self.grid[row,6] = Knight((row,6), color)
            self.grid[row,7] = Rook((row,7), color)

        for c in range(8):
            self.grid[1,c]=Pawn((1,c),'b')

        for c in range(8):
            self.grid[6,c]=Pawn((6,c),'w')

    def update(self): #updates the state of the board after each move
        pass

    def isEmpty(self, pos): #checks if the specified position is empty or not. Empty -> (false). Not Empty -> (true, piece)
        pass

    @staticmethod
    def inBounds(tup):
        return 0<=tup[0]<=7 and 0<=tup[1]<=7

    def legalMovesFrom(self, pos) -> list:
        if self.grid[pos] is None:
            return []
        r,c = pos
        ans = []
        thisColor = self.grid[pos].color
        if isinstance(self.grid[pos],Knight):
            deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr,dc in deltas:
                newpos = (r+dr,c+dc)
                if (Board.inBounds(newpos) and
                        (self.grid[newpos] is None or self.grid[newpos].color != thisColor)):
                    ans.append(newpos)

        return ans

    def __str__(self):
        ans='   0  1  2  3  4  5  6  7\n'
        for i,row in enumerate(self.grid):
            ans += f"{i} "
            for cell in row:
                ans += (' .' if cell==None else str(cell)) + ' '
            ans+='\n'
        return ans
