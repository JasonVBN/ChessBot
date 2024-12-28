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

            # make the move
            captured = self.board.move(start,dest)

            # check if it's mate
            mate = self.board.isMated('w' if color=='b' else 'b')

            # UNDO the move to prep for next candidate move
            self.board.undo(start,dest,captured)

            if mate:
                return True,Move(start,dest)
        return False,Move()

    def findMateInX(self, color, depth):
        # print(f"{'-'*depth} searching for mate in {depth}")
        if depth==1:
            return self.findMateIn1(color)
        for ourmove in self.allLegalMoves(color):
            # print(f"Trying: {ourmove}")
            ourstart, ourdest = ourmove.start, ourmove.dest

            # make the move
            ourcaptured = self.board.move(ourstart,ourdest)

            found = True
            for theirmove in self.allLegalMoves('w' if color == 'b' else 'b'):
                # print(f"- If they go {theirmove}")
                start2, dest2 = theirmove.start, theirmove.dest
                captured2 = self.board.move(start2,dest2)

                mate, nextmove = self.findMateInX(color, depth-1) # recursive call

                self.board.undo(start2,dest2,captured2)

                if not mate:
                    found = False
                    break

            # UNDO the move to prep for next candidate move
            self.board.undo(ourstart, ourdest, ourcaptured)

            if found:
                return True, Move(ourstart, ourdest)
        return False, Move()
