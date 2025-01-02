from Board3 import Board
class Engine:
    def __init__(self, board):
        self.board = board

    def allLegalMoves(self, color):
        return self.board.allLegalMoves(color)
        # just to save a few characters when calling lol

    def allMoves(self,color):
        return self.board.allMoves(color)

    def bestMoveIn1(self, color):
        bestMove = None
        bestEval = -1000
        for move in self.board.allMoves(color):
            # make move
            captured = self.board.move(move)

            # calculate evaluation, update bestMove & bestEval
            e=self.board.ev
            if e > bestEval:
                bestMove = move
                bestEval = e

            # undo move
            self.board.undo(move,captured)
        return bestEval,bestMove

    def bestMoveInX(self,color,depth):
        if depth==1:
            return self.bestMoveIn1(color)
        bestMove = None
        bestEval = -1000
        for ourmove in self.allMoves(color):
            ourcaptured = self.board.move(ourmove)

            minEval = 1000
            for theirmove in self.allMoves('w' if color == 'b' else 'b'):
                theircaptured = self.board.move(theirmove)
                e,move = self.bestMoveInX(color,depth-1)
                self.board.undo(theirmove,theircaptured)
                minEval = min(minEval,e)
                if minEval <= bestEval:
                    break

            if minEval > bestEval:
                bestMove = ourmove
                bestEval = minEval
            self.board.undo(ourmove,ourcaptured)
        return bestEval,bestMove


    # Daddy Srinath's code below

    def bestMove(self, color, depth, maxplayer):
        bM = None
        e = -1000
        for move in self.board.allLegalMoves(color):
            ourcaptured = self.board.move(move)
            evaluat = self.minimax(color, depth, maxplayer)
            if evaluat>e:
                e = evaluat
                bM = move
            self.board.undo(move, ourcaptured)
        return bM
    def minimax(self, color, depth, maxplayer):
        if depth == 1:
            return self.evaluation()
        if maxplayer:
            maxEval = -1000
            for ourmove in self.board.allLegalMoves(color):
                ourcaptured = self.board.move(ourmove)

                e = self.minimax('w', depth-1, False)
                if e > maxEval:
                    maxEval = e

                # undo OUR move
                self.board.undo(ourmove,ourcaptured)
            return maxEval
        else:
            minEval = 1000
            if color == 'w': color = 'b'
            for ourmove in self.board.allLegalMoves(color):
                ourcaptured = self.board.move(ourmove)

                e = self.minimax('b', depth - 1, True)
                if e < minEval:
                    minEval = e
                # undo OUR move
                self.board.undo(ourmove, ourcaptured)
            return minEval