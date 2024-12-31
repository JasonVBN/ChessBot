import numpy as np
from AtomicBoard import ABoard
from ForcedMate import Mater
from Move import Move

custom = np.array([
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.']
        ])

board = ABoard()

print(board)
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")
lastmove = Move()
lastcap = None
while True:
    # if board.isMated('w'): print('white is mated')
    # elif board.isMated('b'): print('black is mated')
    # else: print('no one is mated')

    # print("all legal moves for w:")
    # for move in board.allLegalMoves('w'):
    #     print(move)

    ipt = input("Enter START square: ")
    if ipt=='undo':
        board.undo(lastmove.start,lastmove.dest,lastcap)
        print(board)
        print(board.kingPos)
        continue
    start = (int(ipt[0]), int(ipt[1]))
    legal = board.legalMovesFrom(start)
    print("legal moves:", legal)

    ipt = input("Enter DEST square: ")
    dest = (int(ipt[0]), int(ipt[1]))

    if dest in legal:
        lastcap = board.move(start,dest)
        lastmove.start,lastmove.dest = start,dest
        print(board)
        print(board.kingPos)
    else:
        print("not a legal move!")


    print()