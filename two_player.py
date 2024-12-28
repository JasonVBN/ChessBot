import numpy as np
from Board2 import Board
from ForcedMate import Mater
from Move import Move

board = Board()

print(board)
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")
lastmove = Move()
lastcap = None
while True:
    if board.inCheck('w'): print("white is in check")
    elif board.inCheck('b'): print("black is in check")
    else: print("no one is in check")

    if board.isMated('w'): print('white is mated')
    elif board.isMated('b'): print('black is mated (we love mating black things)')
    else: print('no one is mated')

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