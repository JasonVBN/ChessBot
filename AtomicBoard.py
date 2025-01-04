import numpy as np
from Move import Move


class ABoard:
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
    VALUES = {'wP': 10, 'wN': 30, 'wB': 30, 'wR': 50, 'wQ': 90, 'wK': 1000,
              'bP': -10, 'bN': -30, 'bB': -30, 'bR': -50, 'bQ': -90, 'bK': -1000}
    def __init__(self, setup=DEFAULT_SETUP):
        self.grid = np.array([[None for c in range(8)] for r in range(8)])
        # self.pieceLocations = {'w':[], 'b':[]}
        self.kingAlive = {'w': False, 'b': False}
        for r in range(8):
            for c in range(8):
                if setup[r,c] not in ['', '.', ' ', '--']:    # denote empty squares
                    col,ptype = setup[r,c]
                    # self.pieceLocations[col].append((r,c))
                    self.grid[r,c] = setup[r,c]
                    if ptype=='K':
                        self.kingAlive[col] = True
        self.ev = self.evaluation()
        # print("ATOMIC BOARD using string rep of pieces")

    def evaluation(self,color='w'):
        e=0
        for r in range(8):
            for c in range(8):
                piece = self.grid[r, c]
                if piece is not None:
                    e += self.VALUES[piece]
        return e

    @staticmethod
    def inBounds(tup):
        return 0<=tup[0]<=7 and 0<=tup[1]<=7

    def squaresSeenFrom(self, pos) -> list:
        if self.grid[pos] is None:
            return []
        startR,startC = pos
        ans = []
        piece = self.grid[pos]
        thisColor = piece[0]

        if piece[1]=='P':
            # 4 cases: forward 1, forward 2, take left, take right
            dir = -1 if piece[0]=='w' else +1
            if 0 <= startR+dir <= 7 and self.grid[startR+dir, startC] is None:
                ans.append((startR+dir, startC))    # forward 1
                if ((piece[0]=='w' and startR==6) or
                    (piece[0]=='b' and startR==1)) and self.grid[startR+2*dir, startC] is None:
                    ans.append((startR+2*dir, startC))  # forward 2
            for dc in [-1,1]:
                newpos = (startR+dir, startC+dc)
                if ABoard.inBounds(newpos):
                    diag = self.grid[newpos]
                    if diag is not None and diag[0] != thisColor:
                        ans.append(newpos)

        elif piece[1]=='N' or piece[1]=='K':
            deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)] if piece[1]=='N' \
                else [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr,dc in deltas:
                newpos = (startR+dr,startC+dc)
                if (ABoard.inBounds(newpos) and
                        (self.grid[newpos] is None or self.grid[newpos][0] != thisColor)):
                    ans.append(newpos)

        else: # Bishop (Bitch), Rook, Queen
            deltas = (
                [(1,1), (1,-1), (-1,1), (-1,-1)] if piece[1]=='B' else
                [(1,0), (-1,0), (0,1), (0,-1)] if piece[1]=='R' else
                [(1, 1), (1, -1), (-1, 1), (-1, -1), (1,0), (-1,0), (0,1), (0,-1)]
            )

            for dr,dc in deltas:
                r,c = startR+dr, startC+dc
                while ABoard.inBounds((r,c)):
                    if self.grid[(r,c)] is None:
                        ans.append((r,c))
                    elif self.grid[(r,c)][0] != thisColor:
                        ans.append((r,c))
                        break
                    else:
                        break
                    r, c = r+dr, c+dc
        return ans

    def legalMovesFrom(self, pos) -> list:
        return self.squaresSeenFrom(pos)

    def allLegalMoves(self,color) -> list:
        ans = []
        for r in range(8):
            for c in range(8):
                start=(r,c)
        # for start in self.pieceLocations[color].copy():
                if self.grid[start] is not None and self.grid[start][0] == color:
                    for dest in self.legalMovesFrom(start):
                        ans.append(Move(start,dest))
        return ans

    def allMoves(self,color) -> list:
        ans = []
        for r in range(8):
            for c in range(8):
                start=(r,c)
                if self.grid[start] is not None and self.grid[start][0] == color:
                    for dest in self.squaresSeenFrom(start):
                        ans.append(Move(start,dest))
        return ans

    def isMated(self, color):
        # True if king is dead
        return not self.kingAlive[color]


    # returns list of blown up pieces with their positions
    def move(self, move) -> list:
        start,dest = move.start, move.dest
        pieceToMove = self.grid[start]

        self.grid[start] = None
        if self.grid[dest] == None: # move to empty square - no kaboom
            self.grid[dest] = pieceToMove
            return []
        else: # KABOOOOOOOOOOOOM
            destPiece = self.grid[dest]
            blownup = [(pieceToMove,start), (destPiece,dest)]
            if pieceToMove[1] == 'K':
                self.kingAlive[pieceToMove[0]] = False
            if destPiece[1] == 'K':
                self.kingAlive[destPiece[0]] = False
            self.grid[dest] = None
            deltas = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1,0), (-1,0), (0,1), (0,-1)]
            for dr,dc in deltas:
                boompos = (dest[0]+dr,dest[1]+dc)
                if ABoard.inBounds(boompos):
                    piece = self.grid[boompos]
                    if piece is not None and piece[1] != 'P':     # pawns don't kaboom
                        blownup.append((piece,boompos))
                        self.grid[boompos] = None   # kaboom.
                        if piece[1] == 'K':
                            self.kingAlive[piece[0]] = False
            for piece,pos in blownup:
                self.ev -= self.VALUES[piece]
            return blownup

    def undo(self, move, blownup: list):
        start, dest = move.start, move.dest
        if len(blownup) == 0: # no boom happened
            pieceToMove = self.grid[dest]

            self.grid[dest] = None
            self.grid[start] = pieceToMove
            # no change in eval
        else:
            # place blown-up pieces back
            for piece,pos in blownup:
                self.grid[pos] = piece
                if piece[1]=='K':
                    self.kingAlive[piece[0]] = True
                self.ev += self.VALUES[piece]


    def __str__(self):
        ans='   0  1  2  3  4  5  6  7\n'
        for i,row in enumerate(self.grid):
            ans += f"{i} "
            for cell in row:
                ans += (' .' if cell==None else str(cell)) + ' '
            ans+='\n'
        return ans
