from Board import Board
board = Board()
print(board)
print("Squares are represented by 2-digit sequences [row][col]")
print("For example '00' is top left square, '77' is bottom right square")

ipt = input("Enter START square: ")
start = (int(ipt[0]), int(ipt[1]))

print(board.legalMovesFrom(start))

ipt = input("Enter DEST square: ")
dest = (int(ipt[0]), int(ipt[1]))
# not done yet