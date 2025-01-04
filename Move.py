class Move:
    def __init__(self,start=None,dest=None):
        # start and dest are both tuples
        self.start = start
        self.dest = dest

    @staticmethod
    def tup2coord(tup: tuple) -> str:
        r,c = tup
        return chr(ord('a')+c) + str(8-r)

    def __str__(self):
        # return f"{self.start} -> {self.dest}"
        return f"{self.tup2coord(self.start)} -> {self.tup2coord(self.dest)}"