from bitboard import bitboard
board = bitboard('w')
board.initializeBoard()
#board.visualizer(board.wboard)
#board.visualizer(board.bboard)
board.move('w', 'kn', 'b1', 'c3')
board.move('w', 'p', '')
board.visualizer(board.wboard)