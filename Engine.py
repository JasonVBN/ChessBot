from Board3 import Board
class Engine:
    VALUES = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':100}
    def __init__(self, board):
        self.board = board
        self.pieceValues = {}

        blackpieces=['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
        whitepieces=['wR','wN','wB','wQ','wK','wB','wN','wR', 'wP']
        for p in blackpieces:
            self.pieceValues[p] = -self.VALUES[p[1]]
        for p in whitepieces:
            self.pieceValues[p] = self.VALUES[p[1]]
        print(self.pieceValues)

    def evaluation(self):
        c=0
        for row in self.board.grid:
            for piece in row:
                if piece is not None: c+=self.pieceValues[piece]
        return c

    def bestMoveIn1(self, color):
        bestMove = None
        bestEval = -1000
        for move in self.board.allLegalMoves(color):
            # make move
            captured = self.board.move(move)

            # calculate evaluation & update bestEval
            e=self.evaluation()
            if e > bestEval:
                bestMove = move
                bestEval = e

            # undo move
            self.board.undo(move,captured)
        return bestEval,bestMove

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


    def bestMoveInX_jn(self,color,depth):
        if depth==1:
            return self.bestMoveIn1(color)
        for ourmove in self.board.allLegalMoves(color):
            ourcaptured = self.board.move(ourmove)

