wboard = 0
bboard = 0

class bitboard:
    def __init__(self, color):
        self.wboard = 0 #Bitboard representing state of white pieces
        self.bboard = 0 #Bitboard representing state of black pieces
        self.wboards = {} #Contains bitboards of all white pieces on the board
        self.bboards = {} #Contains bitboards of all black pieces on the board
        self.color = color
    def initializeBoard(self):
        #white pieces
        for i in [chr(j) for j in range(97,105)]:
            self.wboards[self.genPawn(self.calibrate(i+'2'), 'w')]=self.calibrate(i+'2')
        self.wboards[self.genRook(self.calibrate('a1'))]=self.calibrate('a1')
        self.wboards[self.genRook(self.calibrate('h1'))]=self.calibrate('h1')
        self.wboards[self.genKnight(self.calibrate('b1'))] = self.calibrate('b1')
        self.wboards[self.genKnight(self.calibrate('g1'))] = self.calibrate('g1')
        self.wboards[self.genBishopBit(self.calibrate('c1'))] = self.calibrate('c1')
        self.wboards[self.genBishopBit(self.calibrate('f1'))] = self.calibrate('f1')
        self.wboards[self.genQueen(self.calibrate('d1'))] = self.calibrate('d1')
        self.wboards[self.genKing(self.calibrate('e1'))] = self.calibrate('e1')
        self.genBoardBit('w')
        #black pieces
        for i in [chr(j) for j in range(97,105)]:
            self.bboards[self.genPawn(self.calibrate(i+'7'), 'b')]=self.calibrate(i+'7')
        self.bboards[self.genRook(self.calibrate('a8'))]=self.calibrate('a8')
        self.bboards[self.genRook(self.calibrate('h8'))]=self.calibrate('h8')
        self.bboards[self.genKnight(self.calibrate('b8'))] = self.calibrate('b8')
        self.bboards[self.genKnight(self.calibrate('g8'))] = self.calibrate('g8')
        self.bboards[self.genBishopBit(self.calibrate('c8'))] = self.calibrate('c8')
        self.bboards[self.genBishopBit(self.calibrate('f8'))] = self.calibrate('f8')
        self.bboards[self.genQueen(self.calibrate('d8'))] = self.calibrate('d8')
        self.bboards[self.genKing(self.calibrate('e8'))] = self.calibrate('e8')
        self.genBoardBit('b')

    def genBoardBit(self, color):
        if color == 'w':
            for piece in self.wboards:
                self.wboard |=  2**64>>self.wboards[piece]
        elif color == 'b':
            for piece in self.bboards:
                self.bboard |= 2**64>>self.bboards[piece]

    def genBishopBit(self, currentsquare, blocker=0):
        brs = 2 ** 64 >> currentsquare
        directions = [-7, -9, 7, 9]
        for i in directions:
            currentsquare1 = currentsquare
            start1 = currentsquare1
            if currentsquare1 % 8 == 1 and (i == -9 or i == 7):
                continue
            elif currentsquare1 % 8 == 0 and (i == -7 or i == 9):
                continue
            while True:
                if currentsquare1 % 8 != 0 and currentsquare1 % 8 != 1 or (start1 % 8 == 1 and currentsquare1 == start1):
                    if currentsquare1 + i > 0 and currentsquare1 + i < 64:
                        currentsquare1 += i
                    else:
                        break
                else:
                    break
                if blocker & 2 ** 64 >> currentsquare1:
                    break
                brs |= 2 ** 64 >> currentsquare1
        return brs


    def genQueen(self,currentsquare, blocker=0):
        brs = self.genBishopBit(currentsquare, blocker) | self.genRook(currentsquare, blocker)
        return brs


    def genRook(self, currentsquare, blocker=0):
        brs = 2 ** 64 >> currentsquare
        row = currentsquare // 8 if currentsquare % 8 != 0 else currentsquare // 8 - 1  # index from 0
        for i in range((row) * 8 + 1, (row + 1) * 8 + 1):
            if blocker & 2 ** 64 >> i:
                break
            brs |= 2 ** 64 >> i

        directions = [-8, 8]
        for i in directions:
            while True:
                if currentsquare + i > 0 and currentsquare + i <= 64:
                    currentsquare += i
                    if blocker & 2 ** 64 >> currentsquare:
                        break
                    brs |= 2 ** 64 >> currentsquare
                else:
                    break
        return brs

    def genKnight(self, currentsquare):
        brs = 2 ** 64 >> currentsquare
        directions = [-6, -15, -17, -10, 6, 15, 17, 10]
        row = currentsquare // 8 - 1 if currentsquare % 8 == 0 else currentsquare // 8
        col = 7 if currentsquare % 8 == 0 else currentsquare % 8 - 1
        for i in directions:
            if currentsquare + i > 0 and currentsquare + i <= 64:
                row1 = (currentsquare + i) // 8
                col1 = 7 if (currentsquare + i) % 8 == 0 else (currentsquare + i) % 8 - 1
                if row - 2 <= row1 <= row + 2 and col - 2 <= col1 <= col + 2:
                    brs |= 2 ** 64 >> currentsquare + i
        return brs
    def genKing(self, currentsquare, blocker=0):
        directions = [-1, 1, -7, -8, -9, 7, 8, 9]
        brs = 2**64>>currentsquare

        for i in directions:
            if currentsquare % 8 == 1 and (i == -1 or i == -9 or i == 7):
                continue
            elif currentsquare % 8 == 0 and (i == 1 or i == 9 or i == -7):
                continue
            if currentsquare + i > 0 and currentsquare + i < 64:
                if blocker & 2 ** 64 >> currentsquare:
                    break
                brs |= 2 ** 64 >> currentsquare + i
        return brs


    def genPawn(self, currentsquare, color, blocker=0):
        directions = [1, 2]
        row = currentsquare//8
        brs = 2**64 >> currentsquare
        if row == 1 or row == 6:
            brs |= 2**64 >> currentsquare+1 | 2**64 >> currentsquare+2
        else:
            brs |= 2**64 >> currentsquare+1
        if color == 'w':
            row = currentsquare//8
            col = 7 if currentsquare % 8 == 0 else currentsquare % 8 - 1
            for i in self.bboards:
                if self.bboards[i] == currentsquare - 7 :
                    row1 = (currentsquare-7)//8
                    col1 = 7 if (currentsquare-7) % 8 == 0 else (currentsquare-7) % 8 - 1
                    if row-1<=row1<=row+1 and col-1<=col1<=col+1:
                        brs |= 2**64 >> currentsquare-7
                if self.bboards[i] == currentsquare - 9:
                    row1 = (currentsquare-9)//8
                    col1 = 7 if (currentsquare-9)%8 == 0 else (currentsquare-9)%8 - 1
                    if row-1<=row1<=row+1 and col-1<=col1<=col+1:
                        brs |= 2**64 >> currentsquare-9
        return brs
    def calibrate(self, position):
        row = 8-int(position[1])
        col = ord(position[0])-96
        return row*8 + col
    def findpiece(self, position):
        if self.color == 'w':
            for i in self.wboards:
                if self.wboards[i] == position:
                    return i
        else:
            for i in self.bboards:
                if self.bboards[i] == position:
                    return i
    def genPiece(self, color, type, pos):
        if type == 'kn':
            return self.genKnight(pos)
        if type == 'b':
            return self.genBishopBit(pos)
        if type == 'p':
            return self.genPawn(pos, color)
        if type == 'q':
            return self.genQueen(pos)
        if type == 'r':
            return self.genRook(pos)
        if type == 'k':
            return self.genKing(pos)
    def move(self, color, type, startposition, endposition):
        startnumpos = self.calibrate(startposition)
        endnumpos = self.calibrate(endposition)
        bit = self.findpiece(startnumpos)
        #checks if the given end position is valid based on the attack bitboard
        if 2**64>>endnumpos & bit == 2**64>>endnumpos and color == 'w':
            #deletes piece from board and then updates in new place
            self.wboard = 2**64>>startnumpos ^ self.wboard
            self.wboard |= 2**64>>endnumpos
            del self.wboards[bit]
            self.wboards[self.genPiece(color, type, endnumpos)] = endnumpos
        elif 2**64>>endnumpos & bit == 2**64>>endnumpos and color == 'b':
            # deletes piece from board and then updates in new place
            self.bboard = 2 ** 64 >> startnumpos ^ self.wboard
            self.bboard |= 2 ** 64 >> endnumpos
            del self.wboards[bit]
            self.bboards[self.genPiece(color, type, endnumpos)] = endnumpos
    def visualizer(self, bits):
        if bits > 0:
            if len(str(bin(bits))[2:]) == 64:
                c = ''
                for i in range(64):
                    if i % 8 == 0:
                        print(c)
                        c = ''
                    c += str(bin(bits))[2:][i]
                print(c)
            else:
                c = ''
                bits = '0' * (64 - len(str(bin(bits))[2:])) + str(bin(bits))[2:]
                for i in range(64):
                    if i % 8 == 0 and i != 0:
                        print(c)
                        c = ''
                    c += bits[i]
                print(c)
        else:
            if len(str(bin(bits))[3:]) == 64:
                c = ''
                for i in range(64):
                    if i % 8 == 0:
                        print(c)
                        c = ''
                    c += str(bits)[3:][i]
                print(c)
            else:
                c = ''
                bits = '0' * (64 - len(str(bin(bits))[3:])) + str(bin(bits))[3:]
                for i in range(64):
                    if i % 8 == 0 and i != 0:
                        print(c)
                        c = ''
                    c += bits[i]
                print(c)


    def inversion(self, bits):
        c = ''
        for i in str(bin(bits))[3:]:
            c += str([1, 0][int(i)])
        return int('0b' + c, 2)


    def modifyOppBoard(self, board):
        boardc = []
        for i in board:
            boardc.append(i ^ 2 ** 64 >> board[i][0])
        return boardc


    def isMated(self, kingbit, kingpos, color):
        original = kingbit
        twocopy = kingbit
        if color == 'w':
            b = 0
            board = self.modifyOppBoard(self.bboards)
            for i in board:
                b |= i
            kingbit = b ^ kingbit
            # visualizer(kingbit)
            w = 0
            for i in self.wboards:
                w |= i
            kingbit = (w | kingbit)
            twocopy |= kingbit
        if (twocopy) ^ kingbit == original:
            return True
        return False