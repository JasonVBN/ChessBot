from Move import Move

class Mater:
    def __init__(self, board):
        self.board = board

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
            # make the move
            captured = self.board.move(move)

            # check if it's mate
            mate = self.board.isMated('w' if color=='b' else 'b')

            # UNDO the move to prep for next candidate move
            self.board.undo(move,captured)

            if mate:
                return True,move
        return False,Move()

    def findMateInX(self, color, depth):
        # print(f"{'-'*depth} searching for mate in {depth}")
        if depth==1:
            return self.findMateIn1(color)
        for ourmove in self.allLegalMoves(color):
            # print(f"Trying: {ourmove}")
            ourcaptured = self.board.move(ourmove)

            found = True
            for theirmove in self.allLegalMoves('w' if color == 'b' else 'b'):
                captured2 = self.board.move(theirmove)
                mate, nextmove = self.findMateInX(color, depth-1) # recursive call
                self.board.undo(theirmove,captured2)

                if not mate:
                    found = False
                    break

            self.board.undo(ourmove, ourcaptured)

            if found:
                return True, ourmove
        return False, Move()
