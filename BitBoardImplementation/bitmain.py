from bitboard import bitboard
board = bitboard('w')
board.wboards = {board.genKing(5):5,board.genQueen(4):4, board.genBishopBit(6):6, board.genPawn(13,'w'):13, board.genPawn(12,'w'):12}
board.bboards = {board.genBishopBit(14):14, board.genKnight(29):29}
#print(board.wboard)
board.genBoardBit('w')
board.genBoardBit('b')
board.wboards = {board.genKing(5):5,board.genQueen(4):4, board.genBishopBit(6):6, board.genPawn(13,'w'):13, board.genPawn(12,'w'):12}
board.bboards = {board.genBishopBit(14):14, board.genKnight(29):29}
#board.visualizer(2**64>>14&(board.wboard^2**64>>5) )
#board.visualizer(2**64>>14)
#board.visualizer(board.genKing(5,board.wboard^2**64>>5))
#board.visualizer(board.wboard^2**64>>5)
board.visualizer(board.genKing(14, board.wboard^2**64>>14))
print('te')
w=0
for i in board.wboards:
    w |= i
board.visualizer(w)
print('stop')
#board.visualizer(w & 2**64>>board.bboards[board.genRook(8)])
print('stop')
board.visualizer(board.wboard)
print(board.goog(w))
board.visualizer(board.bboard)
