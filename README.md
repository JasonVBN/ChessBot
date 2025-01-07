*Work-in-progress*

Collaboration between [Jason](https://github.com/JasonVBN) & [Srinath](https://github.com/srinpin05)

Our own chess engine. Currently, it calculates to a depth of 3 moves (technically can do any depth, but very slow for depths beyond 3) and can find any forced mate within 3 moves. When no forced mate is found, we evaluate position based on material count (standard point system: pawn=1, knight=3, bishop=3, rook=5, queen=9), and giving more points to well-placed pieces (e.g. in center of board, rooks on open files).
