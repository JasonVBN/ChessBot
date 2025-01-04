import time
import numpy as np
from Board3 import Board
from Engine import Engine
from Move import Move

DEPTH = 3
COLOR = input("Computer color (w or b): ")
assert COLOR in ['w','b']

board = Board()
print(board)
eng = Engine(board)

def coord2tup(coord: str):
    assert len(coord)==2
    c,r = coord
    return (8-int(r), ord(c)-ord('a'))

lastmove = Move()
lastcap = None
while True:
    print(f"\ncalculating for depth {DEPTH}...")

    print("current eval:",board.evaluation())
    startTime = time.time()
    bestEval,move,line = eng.bestMoveInX(COLOR,DEPTH)
    print(f"engine move: {move} | eval with depth {DEPTH}: {bestEval}")
    elapsedTime = time.time()-startTime
    print(f"computing time: {elapsedTime}")

    board.move(move)

    print(board)
    ipt = input("Enter START square: ")
    if ipt == 'undo':
        board.undo(lastmove, lastcap)
        print(board)
        print(board.kingPos)
        continue
    start = coord2tup(ipt)
    legal = board.squaresSeenFrom(start)
    print("legal moves:", legal)

    ipt = input("Enter DEST square: ")
    dest = coord2tup(ipt)
    while dest not in legal:
        print("not a legal move!")
        ipt = input("Enter DEST square: ")
        dest = coord2tup(ipt)

    lastcap = board.move(Move(start, dest))
    lastmove.start, lastmove.dest = start, dest
    print(board)
    print(board.kingPos)