import time
from tkinter import *
import numpy as np
from Board3 import Board
from Engine import Engine
from Presets import *

DEPTH = 4

root = Tk()
root.geometry("500x300")

setup = np.array([['' for c in range(8)] for r in range(8)])

cells = [[None for c in range(8)] for r in range(8)]

FONT = ('Arial', 12, 'bold')

### SETUP THE GRID ###

for c in range(8): # header row
    e = Entry(root, width=4,font=FONT)
    e.grid(row=0, column=c+1)
    e.insert(END, chr(ord('a')+c))
for r in range(8):
    e = Entry(root, width=4,font=FONT)
    e.grid(row=r+1, column=0)
    e.insert(END, str(8-r))
    for c in range(8):
        e = Entry(root, width=4,font=FONT)
        e.grid(row=r+1, column=c+1)
        val = setup[r,c]
        e.insert(END,'.' if val is None else str(val))
        cells[r][c] = e

def update(board):
    for r in range(8):
        for c in range(8):
            e = cells[r][c]
            e.delete(0,last=len(e.get()))
            newval = board.grid[r,c]
            e.insert(END, '' if newval is None else str(newval))

### THIS IS THE PRIMARY FUNCTION
def solve(color):
    DEPTH = int(eDepth.get())
    print(f"\ncalculating for depth {DEPTH}...")
    setup = np.array([[cells[r][c].get() for c in range(8)] for r in range(8)])
    board = Board(setup=setup)

    eng = Engine(board)
    print("current eval:",board.evaluation())
    startTime = time.time()
    bestEval,move,line = eng.bestMoveInX(color,DEPTH)
    print(f"engine move: {move} | eval with depth {DEPTH}: {bestEval}")
    for m in line: print(m)
    elapsedTime = time.time()-startTime
    print(f"computing time: {elapsedTime}")

    board.move(move)
    update(board)

eDepth = Entry(root, width=4,font=FONT)
eDepth.grid(row=10, column=0, columnspan=3)

B=Button(root, text="Play White move", command=lambda:solve('w'))
B.grid(row=10,column=3,columnspan=3)

B=Button(root, text="Play Black move", command=lambda:solve('b'))
B.grid(row=10,column=6,columnspan=3)

Bclear=Button(root, text="Clear", command=lambda:update(Board(EMPTY)))
Bclear.grid(row=11,column=3,columnspan=3)

def setup_damiano():
    update(Board(
        np.array([
            ['.', '.', '.', '.', '.', 'bR', 'bK', '.'],
            ['.', '.', '.', '.', '.', 'bP', 'bP', '.'],
            ['.', '.', '.', '.', '.', '.', 'wP', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'wK', '.', '.', 'wQ', 'wR']
        ])
    ))

def setup_smother():
    update(Board(
        np.array([
            ['.', '.', '.', '.', 'bR', '.', '.', 'bK'],
            ['.', '.', '.', '.', '.', '.', 'bP', 'bP'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'wQ', '.', '.', 'wN', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'wK', '.', '.', '.', '.']
        ])
    ))

B2=Button(root, text="starting position", command=lambda:update(Board(STARTING)))
B2.grid(row=11,column=0,columnspan=3)

B3=Button(root, text="Setup: backrank M2", command=lambda:update(Board(BACKRANK_M2)))
B3.grid(row=12,column=6,columnspan=3)

B5=Button(root, text="Setup: Damiano M3", command=setup_damiano)
B5.grid(row=12,column=0,columnspan=3)

B6=Button(root, text="Setup: Smothered M4", command=setup_smother)
B6.grid(row=12,column=3,columnspan=3)

root.mainloop()
