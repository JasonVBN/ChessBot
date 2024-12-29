import numpy as np

from Move import Move
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen
from King import King

class Board:
    DEFAULT_SETUP = np.array([
        ['bR','bN','bB','bQ','bK','bB','bN','bR'],
        ['bP','bP','bP','bP','bP','bP','bP','bP'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['wP','wP','wP','wP','wP','wP','wP','wP'],
        ['wR','wN','wB','wQ','wK','wB','wN','wR']
    ])
    encoding = {'P':Pawn,'N':Knight,'B':Bishop,'R':Rook,'Q':Queen,'K':King}
    def __init__(self, setup=DEFAULT_SETUP):
        self.kingPos = { 'w':(7,4), 'b':(0,4) }
        self.grid = np.array([[None for c in range(8)] for r in range(8)])
        self.pieceLocations = {'w':[], 'b':[]}
        for r in range(8):
            for c in range(8):
                if setup[r,c] not in ['', '.', ' ']:    # denote empty squares
                    col,ptype = setup[r,c]
                    self.pieceLocations[col].append((r,c))
                    newpiece = Board.encoding[ptype]((r,c),col)
                    self.grid[r,c] = newpiece
                    if isinstance(newpiece,King):
                        self.kingPos[newpiece.color] = (r,c)
        print(self.pieceLocations)

    def isEmpty(self, pos): #checks if the specified position is empty or not. Empty -> (false). Not Empty -> (true, piece)
        pass

    @staticmethod
    def inBounds(tup):
        return 0<=tup[0]<=7 and 0<=tup[1]<=7

    def doesntWalkIntoMate(self, start, dest):
        # make the move
        captured = self.move(start,dest)

        # check whether inCheck
        inCheck = self.inCheck(self.grid[dest].color)

        # UNDO the move
        self.undo(start,dest,captured)

        return not inCheck

    def squaresSeenFrom(self, pos) -> list:
        if self.grid[pos] is None:
            return []
        startR,startC = pos
        ans = []
        piece = self.grid[pos]
        thisColor = piece.color

        if isinstance(piece,Pawn):
            '''
            4 cases:
            forward 1, forward 2 (if on starting row - 6 for white, 1 for black)
            take left, take right
            '''
            dir = -1 if piece.color=='w' else +1
            if 0 <= startR+dir <= 7 and self.grid[startR+dir, startC] is None:
                ans.append((startR+dir, startC))    # forward 1
                if ((piece.color=='w' and startR==6) or
                    (piece.color=='b' and startR==1)) and self.grid[startR+2*dir, startC] is None:
                    ans.append((startR+2*dir, startC))  # forward 2
            for dc in [-1,1]:
                newpos = (startR+dir, startC+dc)
                if Board.inBounds(newpos):
                    diag = self.grid[newpos]
                    if diag is not None and diag.color != thisColor:
                        ans.append(newpos)

        elif isinstance(piece,Knight):
            deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr,dc in deltas:
                newpos = (startR+dr,startC+dc)
                if (Board.inBounds(newpos) and
                        (self.grid[newpos] is None or self.grid[newpos].color != thisColor)):
                    ans.append(newpos)
        elif isinstance(piece, King):
            deltas = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr,dc in deltas:
                newpos = (startR+dr,startC+dc)
                if (Board.inBounds(newpos) and
                        (self.grid[newpos] is None or self.grid[newpos].color != thisColor)):
                    ans.append(newpos)

        else: # Bishop (Bitch), Rook, Queen
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

    def legalMovesFrom(self, pos) -> list:
        return [dest for dest in self.squaresSeenFrom(pos) if self.doesntWalkIntoMate(pos,dest)]

    def allLegalMoves(self,color) -> list:
        ans = []
        # for r in range(8):
        #     for c in range(8):
        #         start=(r,c)
        for start in self.pieceLocations[color].copy():
            if self.grid[start] is not None and self.grid[start].color == color:
                for dest in self.legalMovesFrom(start):
                    ans.append(Move(start,dest))
        return ans

    def move(self, start, dest):
        pieceToMove = self.grid[start]
        # if we're moving a King, update kingPos:
        if isinstance(pieceToMove,King):
            self.kingPos[pieceToMove.color] = dest

        captured = self.grid[dest]
        self.grid[dest] = pieceToMove
        self.grid[start] = None

        arr = self.pieceLocations[pieceToMove.color]
        arr[arr.index(start)] = dest
        if captured is not None:
            otherColor = 'w' if pieceToMove.color=='b' else 'b'
            self.pieceLocations[otherColor].remove(dest)
        return captured

    def undo(self, start, dest, captured):
        pieceToMove = self.grid[dest]
        # if we're moving a King, update kingPos:
        if isinstance(pieceToMove, King):
            self.kingPos[pieceToMove.color] = start

        self.grid[start] = pieceToMove
        self.grid[dest] = captured

        arr = self.pieceLocations[pieceToMove.color]
        arr[arr.index(dest)] = start
        if captured is not None:
            otherColor = 'w' if pieceToMove.color=='b' else 'b'
            self.pieceLocations[otherColor].append(dest)

    # original (brute force) version of inCheck. not used.
    def inCheckSlow(self, color) -> bool:
        '''
        go thru all pieces of the opposite color as *color*.
        run squaresSeenFrom() on that square.
        if any of those squares contain King, return True
        '''
        for r in range(8):
            for c in range(8):
                if self.grid[r, c] is not None and self.grid[r, c].color != color:
                    squaresHit = self.squaresSeenFrom((r, c))
                    for pos in squaresHit:
                        if pos == self.kingPos[color]:
                            return True
        return False

    def inCheck(self, color) -> bool:
        assert color == 'w' or color == 'b'

        kRow,kCol = self.kingPos[color]
        deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr,dc in deltas:
            if Board.inBounds((kRow+dr,kCol+dc)):
                piece = self.grid[kRow+dr,kCol+dc]
                if (isinstance(piece,Knight) and piece.color != color):
                    return True

        deltas = [(-1,-1),(-1,1)] if color=='w' else [(1,-1),(1,1)]
        for dr,dc in deltas:
            if Board.inBounds((kRow+dr,kCol+dc)):
                piece = self.grid[kRow+dr,kCol+dc]
                if (isinstance(piece,Pawn) and piece.color != color):
                    return True

        deltas = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in deltas:
            if Board.inBounds((kRow + dr, kCol + dc)):
                piece = self.grid[kRow + dr, kCol + dc]
                if (isinstance(piece, King) and piece.color != color):
                    return True

        deltas = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # diagonals
        for dr,dc in deltas:
            r, c = kRow + dr, kCol + dc
            while Board.inBounds((r, c)):
                piece = self.grid[r,c]
                if piece is not None:
                    if isinstance(piece,(Bishop,Queen)) and piece.color != color:
                        return True
                    break
                r, c = r + dr, c + dc

        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)] # horiz/vert
        for dr,dc in deltas:
            r, c = kRow + dr, kCol + dc
            while Board.inBounds((r, c)):
                piece = self.grid[r,c]
                if piece is not None:
                    if isinstance(piece,(Rook,Queen)) and piece.color != color:
                        return True
                    break
                r, c = r + dr, c + dc

        return False

    def isMated(self, color):
        '''
        pseudo-code:
        WLOG let's say color is 'w' (we're checking if white is checkmated)
        try all possible moves that white can make
        and if white is still in check after all of those moves, it's mate!
        '''

        # lol nevermind. much easier way:

        if not self.inCheck(color): return False
        return len(self.allLegalMoves(color)) == 0

    def __str__(self):
        ans='   0  1  2  3  4  5  6  7\n'
        for i,row in enumerate(self.grid):
            ans += f"{i} "
            for cell in row:
                ans += (' .' if cell==None else str(cell)) + ' '
            ans+='\n'
        return ans
