class Move:
    def __init__(self,start=None,dest=None):
        # start and dest are both tuples
        self.start = start
        self.dest = dest

    def __str__(self):
        return f"{self.start} -> {self.dest}"