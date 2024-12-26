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
        startR,startC = pos
        ans = []
        piece = self.grid[pos]
        thisColor = piece.color

        if isinstance(piece,Knight):
            deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr,dc in deltas:
                newpos = (startR+dr,startC+dc)
                if (Board.inBounds(newpos) and
                        (self.grid[newpos] is None or self.grid[newpos].color != thisColor)):
                    ans.append(newpos)
        elif isinstance(piece,Pawn):
            '''
            4 cases:
            forward 1
            forward 2 (if on starting row - 6 for white, 1 for black)
            take left
            take right
            '''
            dir = -1 if piece.color=='w' else +1
            if self.grid[startR+dir, startC] is None:
                ans.append((startR+dir, startC))
                if self.grid[startR+2*dir, startC] is None:
                    ans.append((startR+2*dir, startC))
            if startC-1 >= 0:
                diagLeft = self.grid[startR+dir, startC-1]
                if diagLeft is not None and diagLeft.color != thisColor:
                    ans.append((startR+dir, startC-1))
            if startC+1 <= 7:
                diagRight = self.grid[startR+dir, startC+1]
                if diagRight is not None and diagRight.color != thisColor:
                    ans.append((startR+dir, startC+1))

        else: # Bishop (aka Bitch), Rook, Queen
            deltas = (
                [(1,1), (1,-1), (-1,1), (-1,-1)] if isinstance(piece,Bishop) else
                [(1,0), (-1,0), (0,1), (0,-1)] if isinstance(piece,Rook) else
                [(1, 1), (1, -1), (-1, 1), (-1, -1), (1,0), (-1,0), (0,1), (0,-1)]
            )

            for dr,dc in deltas:
                r,c = startR+dr, startC+dc
                while Board.inBounds((r,c)):
                    if self.grid[(r,c)] is None:
                        ans.append((r,c))
                    elif self.grid[(r,c)].color != thisColor:
                        ans.append((r,c))
                        break
                    else:
                        break
                    r, c = r+dr, c+dc

        return ans

    def move(self, start, dest):
        self.grid[dest] = self.grid[start]
        self.grid[start] = None

    def __str__(self):
        ans='   0  1  2  3  4  5  6  7\n'
        for i,row in enumerate(self.grid):
            ans += f"{i} "
            for cell in row:
                ans += (' .' if cell==None else str(cell)) + ' '
            ans+='\n'
        return ans
