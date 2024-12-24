import numpy as np
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen
class Board:
    def __init__(self):
        self.board = np.array([[None for c in range(8)] for r in range(8)])

        self.board[0,0]=Rook((0,0),'b')
        self.board[0,1]=Knight((0,1),'b')
        # this is so f---ing tedious
        # will do later
        for c in range(8):
            self.board[1,c]=Pawn((1,c),'b')

    def update(self): #updates the state of the board after each move
        pass

    def isEmpty(self, pos): #checks if the specified position is empty or not. Empty -> (false). Not Empty -> (true, piece)
        pass

    def __str__(self):
        ans=''
        for row in self.board:
            for cell in row:
                if cell==None:
                    ans+='.'
                else:
                    ans+=str(cell)
            ans+='\n'
        return ans
