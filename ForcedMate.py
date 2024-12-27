from Board2 import Board
from Move import Move


class Mater:
    def __init__(self, board):
        self.board = board

    def get(self,pos):
        return self.board.grid[pos]

    def set(self,pos,piece):
        self.board.grid[pos] = piece

    def allLegalMoves(self, color):
        return self.board.allLegalMoves(color)
        # just to save a few characters when calling lol

    def findMate(self, color, depth):
        for n in range(1,depth+1):
            found, move = self.findMateInX(color,n)
            if found:
                return True, move, n

        return False,Move(),-1

    def findMateIn1(self, color):
        for move in self.allLegalMoves(color):
            start,dest = move.start,move.dest
            captured = self.board.grid[dest]

            # make the move
            self.board.grid[dest] = self.board.grid[start]
            self.board.grid[start] = None

            # check if it's mate
            mate = self.board.isMated('w' if color=='b' else 'b')

            # UNDO the move to prep for next candidate move
            self.board.grid[start] = self.board.grid[dest]
            self.board.grid[dest] = captured

            if mate:
                return True,Move(start,dest)
        return False,Move()

    def findMateInX(self, color, depth):
        if depth>=3: print(f"{'-'*depth} searching for mate in {depth}")
        if depth==1:
            return self.findMateIn1(color)
        for ourmove in self.allLegalMoves(color):
            print(f"Trying: {ourmove}")
            ourstart, ourdest = ourmove.start, ourmove.dest
            ourcaptured = self.board.grid[ourdest]

            # make the move
            self.board.grid[ourdest] = self.board.grid[ourstart]
            self.board.grid[ourstart] = None

            found = True
            for theirmove in self.allLegalMoves('w' if color == 'b' else 'b'):
                # print(f"- If they go {theirmove}")
                start2, dest2 = theirmove.start, theirmove.dest
                captured2 = self.get(dest2)
                self.board.grid[dest2] = self.get(start2)
                self.board.grid[start2] = None

                mate, nextmove = self.findMateInX(color, depth-1)

                self.board.grid[start2] = self.board.grid[dest2]
                self.board.grid[dest2] = captured2

                if not mate:
                    found = False
                    break

            # UNDO the move to prep for next candidate move
            self.board.grid[ourstart] = self.board.grid[ourdest]
            self.board.grid[ourdest] = ourcaptured

            if found:
                return True, Move(ourstart, ourdest)
        return False, Move()
