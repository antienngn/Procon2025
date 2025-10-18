import numpy as np

class PairSolver:
    def __init__(self):
        self.n = None
        self.board = None
        self.paired = None
        self.ops = []

    def rotate(self, x, y, k):
        """
        Rotate sub-square of size k at top-left (x,y) clockwise.
        """
        B = self.board
        tmp = B[x:x+k, y:y+k].copy()
        # Perform clockwise rotation
        for i in range(k):
            for j in range(k):
                B[x+j, y+k-1-i] = tmp[i, j]
        self.ops.append({'x': x, 'y': y, 'n': k})

    def find_partner(self, x, y):
        """
        Find coordinates of unmatched partner of B[x][y].
        """
        v = self.board[x, y]
        for i in range(self.n):
            for j in range(self.n):
                if not self.paired[i, j] and (i, j) != (x, y) and self.board[i, j] == v:
                    return (i, j)
        return None

    def move_towards(self, sx, sy, tx, ty):
        """
        Slide element at (sx, sy) towards (tx, ty) using 2×2 rotations.
        """
        while sy < ty - 1:
            self.rotate(sx if sx+1 < self.n else sx-1, sy, 2)
            sy += 1
        while sy > ty + 1:
            self.rotate(sx if sx+1 < self.n else sx-1, sy-1, 2)
            sy -= 1
        while sx < tx:
            self.rotate(sx, sy if sy+1 < self.n else sy-1, 2)
            sx += 1
        while sx > tx:
            self.rotate(sx-1, sy if sy+1 < self.n else sy-1, 2)
            sx -= 1
        return sx, sy

    def solve(self, matrix: np.ndarray):
        """
        Solve pairing on a square numpy matrix. Returns list of rotation ops.
        """
        # Initialize board and state
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Input must be a square 2D numpy array")
        self.n = matrix.shape[0]
        self.board = matrix.copy()
        self.paired = np.zeros((self.n, self.n), dtype=bool)
        self.ops = []

        # Main pairing loop
        for i in range(self.n):
            for j in range(self.n):
                if self.paired[i, j]:
                    continue
                partner = self.find_partner(i, j)
                if partner is None:
                    continue
                pi, pj = partner
                # Determine adjacent target position
                if j+1 < self.n and not self.paired[i, j+1]:
                    ti, tj = i, j+1
                else:
                    ti, tj = i, j-1
                # Move partner into place
                ni, nj = self.move_towards(pi, pj, ti, tj)
                # Mark as paired
                self.paired[i, j] = True
                self.paired[ni, nj] = True

        return self.ops

# Example usage:
if __name__ == '__main__':
    import numpy as np
    # Define a sample board
    board = np.array([
        [5,5,7,2],
        [0,3,6,0],
        [4,7,2,4],
        [1,6,3,1]
    ])
    solver = PairSolver()
    ops = solver.solve(board)
    print("Rotation ops:")
    for op in ops:
        print(op)
