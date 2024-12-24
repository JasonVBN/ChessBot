class Piece:
    def __init__(self, pos : (int,int), color : str):
        self.pos = pos
        self.alive = True
        self.color = color # 'w' or 'b'

    def possibleMoves(self) -> list:
        return None

    def move(self, newpos) -> bool:
        self.pos = newpos