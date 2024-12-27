import numpy as np
from Board2 import Board
from ForcedMate import Mater


board = Board()

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