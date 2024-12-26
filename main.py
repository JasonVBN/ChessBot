import numpy as np

from Board2 import Board
from ForcedMate import Mater
from Pawn import Pawn
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen

setup = np.array([
    ['bR','.','.','.','.','.','bK','.'],
    ['.','.','.','.','.','bP','bP','bP'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','wR','.','.','.','.','.'],
    ['.','.','wR','.','.','.','wK','.']
])
# setup = np.array([
#     ['.','.','.','.','.','bR','bK','.'],
#     ['.','.','.','bP','.','.','bP','.'],
#     ['.','.','.','.','bP','.','wP','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','wK','wQ','.','.','.','wR']
# ])
# setup = np.array([
#     ['.','.','.','.','bR','.','.','.'],
#     ['.','.','.','.','.','.','.','.'],
#     ['.','.','bP','.','bR','.','wP','.'],
#     ['.','.','wB','.','.','.','.','.'],
#     ['bK','wP','.','wP','.','.','.','.'],
#     ['.','.','.','wK','bN','.','.','wP'],
#     ['.','.','wP','.','wR','.','wP','.'],
#     ['.','.','.','.','wR','.','.','.']
# ])
board = Board(setup=setup)

print(board)
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")

while True:
    if board.inCheck('w'): print("white is in check")
    elif board.inCheck('b'): print("black is in check")
    else: print("no one is in check")

    if board.isMated('w'): print('white is mated')
    elif board.isMated('b'): print('black is mated (we love mating black things)')
    else: print('no one is mated')

    mater = Mater(board)

    found,move = mater.findMateIn1('w')
    if found: print(f"mate in 1 found for w: {move}")
    else:
        print("no mate in 1 found")
        found, move = mater.findMateIn2('w')
        if found: print(f"mate in 2 found for w, starting with: {move}")
        else:
            print("no mate in 2 found")
            found, move = mater.findMateIn3('w')
            if found: print(f"mate in 3 found for w, starting with: {move}")
            else: print("no mate in 3 found")

    ipt = input("Enter START square: ")
    start = (int(ipt[0]), int(ipt[1]))
    legal = board.legalMovesFrom(start)
    print("legal moves:", legal)

    ipt = input("Enter DEST square: ")
    dest = (int(ipt[0]), int(ipt[1]))
    print(board)
    if dest in legal:
        board.move(start,dest)
        print(board)
    else:
        print("not a legal move!")

    print()