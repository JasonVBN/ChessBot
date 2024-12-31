import time
from tkinter import *
import numpy as np
from Board3 import Board
from ForcedMate import Mater

root = Tk()
root.geometry("500x300")

setup = np.array([['' for c in range(8)] for r in range(8)])

cells = [[None for c in range(8)] for r in range(8)]

FONT = ('Arial', 12, 'bold')

for c in range(8):
    e = Entry(root, width=5,font=FONT)
    e.grid(row=0, column=c+1)
    e.insert(END, c)
for r in range(1,9):
    e = Entry(root, width=5,font=FONT)
    e.grid(row=r, column=0)
    e.insert(END, r-1)
    for c in range(1,9):
        e = Entry(root, width=5,font=FONT)
        e.grid(row=r, column=c)
        val = setup[r-1,c-1]
        e.insert(END,'.' if val is None else str(val))
        cells[r-1][c-1] = e

def update(board):
    for r in range(8):
        for c in range(8):
            e = cells[r][c]
            e.delete(0,last=len(e.get()))
            newval = board.grid[r,c]
            e.insert(END, '' if newval is None else str(newval))

def solve():
    setup = np.array([[cells[r][c].get() for c in range(8)] for r in range(8)])
    board = Board(setup=setup)

    mater = Mater(board)

    startTime = time.time()
    found, move, n = mater.findMate('w', 4)
    if found:
        print(f"mate in {n} found starting with: {move}")
    else:
        print("no mate found :(")
    elapsedTime = time.time()-startTime
    print(f"computing time: {elapsedTime}")

    board.move(move)
    update(board)

B=Button(root, text="Solve!", command=solve)
B.grid(row=10,column=0,columnspan=3)

def setup_empty():
    update(Board(
        np.array([
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.']
        ])
    ))

Bclear=Button(root, text="Clear", command=setup_empty)
Bclear.grid(row=10,column=3,columnspan=3)

def setup_br2():
    update(Board(
        np.array([
            ['bR','.','.','.','.','.','bK','.'],
            ['.','.','.','.','.','bP','bP','bP'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','wR','.','.','.','.','.'],
            ['.','.','wR','.','.','.','wK','.']
        ])
    ))

def setup_br4():
    update(Board(
        np.array([
            ['bR','bR','.','.','.','.','bK','.'],
            ['.','.','.','.','.','bP','bP','bP'],
            ['bQ','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','wR','.','.','.','.','.'],
            ['.','.','wR','.','.','.','.','.'],
            ['.','.','wR','.','.','.','.','.'],
            ['.','.','wR','.','.','.','wK','.']
        ])
    ))

def setup_start():
    update(Board(
        np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ])
    ))

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

B2=Button(root, text="Setup: starting position", command=setup_start)
B2.grid(row=11,column=0,columnspan=3)

B3=Button(root, text="Setup: backrank M2", command=setup_br2)
B3.grid(row=11,column=3,columnspan=3)

B4=Button(root, text="Setup: backrank M4", command=setup_br4)
B4.grid(row=11,column=6,columnspan=3)

B5=Button(root, text="Setup: Damiano M3", command=setup_damiano)
B5.grid(row=12,column=0,columnspan=3)

B6=Button(root, text="Setup: Smothered M4", command=setup_smother)
B6.grid(row=12,column=3,columnspan=3)

root.mainloop()
