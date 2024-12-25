from Board import Board
board = Board()
print(board)
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")

while True:
    ipt = input("Enter START square: ")
    start = (int(ipt[0]), int(ipt[1]))
    legal = board.legalMovesFrom(start)
    print("legal moves:", legal)

    ipt = input("Enter DEST square: ")
    dest = (int(ipt[0]), int(ipt[1]))

    if dest in legal:
        board.move(start,dest)
    else:
        print("not a legal move!")
    print(board)