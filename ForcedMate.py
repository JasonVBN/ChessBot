from Board2 import Board
from Move import Move


class Mater:
    def __init__(self, board):
        self.board = board

    def get(self,pos):
        return self.board.grid[pos]

    def set(self,pos,piece):
        self.board.grid[pos] = piece

    def allLegalMoves(self,color) -> list:
        ans = []
        for r in range(8):
            for c in range(8):
                start=(r,c)
                if self.get(start) is not None and self.get(start).color == color:
                    for dest in self.board.legalMovesFrom(start):
                        ans.append(Move(start,dest))
        return ans

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

    def findMateIn2(self, color):
        print("SEARCHING FOR MATE IN 2...")
        for ourmove in self.allLegalMoves(color):
            # print(f"Trying: {ourmove}")
            ourstart,ourdest = ourmove.start,ourmove.dest
            ourcaptured = self.board.grid[ourdest]

            # make the move
            self.board.grid[ourdest] = self.board.grid[ourstart]
            self.board.grid[ourstart] = None

            found = True
            for theirmove in self.allLegalMoves('w' if color=='b' else 'b'):
                # print(f"- If they go {theirmove}")
                start2,dest2 = theirmove.start,theirmove.dest
                captured2 = self.get(dest2)
                self.board.grid[dest2] = self.get(start2)
                self.board.grid[start2] = None
                
                mate,nextmove = self.findMateIn1(color)
                if not mate:
                    found = False

                self.board.grid[start2] = self.board.grid[dest2]
                self.board.grid[dest2] = captured2

            # UNDO the move to prep for next candidate move
            self.board.grid[ourstart] = self.board.grid[ourdest]
            self.board.grid[ourdest] = ourcaptured

            if found:
                return True,Move(ourstart,ourdest)
        return False,Move()

    def findMateIn3(self, color):
        print("SEARCHING FOR MATE IN 3...")
        for ourmove in self.allLegalMoves(color):
            # print(f"Trying: {ourmove}")
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

                mate, nextmove = self.findMateIn2(color)
                if not mate:
                    found = False

                self.board.grid[start2] = self.board.grid[dest2]
                self.board.grid[dest2] = captured2

            # UNDO the move to prep for next candidate move
            self.board.grid[ourstart] = self.board.grid[ourdest]
            self.board.grid[ourdest] = ourcaptured

            if found:
                return True, Move(ourstart, ourdest)
        return False, Move()