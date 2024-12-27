import numpy as np
import time
from Board2 import Board
from ForcedMate import Mater
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen

# back rank mate in 2:
# setup = np.array([
#     ['bR','.','.','.','.','.','bK','.'],
#     ['.','.','.','.','.','bP','bP','bP'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','wR','.','.','.','.','.'],
#     ['.','.','wR','.','.','.','wK','.']
# ])

# rook sac mate in 3:
setup = np.array([
    ['.','.','.','.','.','bR','bK','.'],
    ['.','.','.','bP','.','.','bP','.'],
    ['.','.','.','.','bP','.','wP','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','wK','wQ','.','.','.','wR']
])

board = Board(setup=setup)

print("Computer is white, you are black")
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")

print(board)

turn = 'w'
while True:
    if turn == 'w':
        startTime = time.time()
        mater = Mater(board)

        found, move, n = mater.findMate('w',3)
        if found:
            print(f"mate in {n} found starting with: {move}")
        else:
            print("no mate found :(")

        board.move(move.start, move.dest)
        elapsedTime = time.time() - startTime
        print(f"Move time: {elapsedTime}")
        turn = 'b'
    else:
        print("Computer has made its move. Your turn!")

        while True:
            ipt = input("Enter START square: ")
            start = (int(ipt[0]), int(ipt[1]))
            legal = board.legalMovesFrom(start)
            if len(legal) == 0:
                print("no legal moves from here!")
                continue

            print("legal moves:", legal)

            ipt = input("Enter DEST square: ")
            dest = (int(ipt[0]), int(ipt[1]))
            print(board)
            if dest in legal:
                board.move(start, dest)
                break
            else:
                print("not a legal move!")
        turn = 'w'

    print(board)

    if board.isMated('w'):
        print('BLACK WINS')
        break
    elif board.isMated('b'):
        print('WHITE WINS')
        break

    if board.inCheck('w'): print("white is in check")
    elif board.inCheck('b'): print("black is in check")
    else: print("no one is in check")

    print()