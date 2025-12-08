


#!/usr/bin/env python3

import math

# ---- Disjoint Set Union ----
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, a):
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

# ---- Read input ----
def read_points(filename):
    pts = []
    with open(filename, "r") as f:
        for line in f:
            if line.strip():
                x, y, z = map(int, line.strip().split(","))
                pts.append((x, y, z))
    return pts

def main():
    points = read_points("E:\Advent of Code\AOC 25\Day-08\input.txt")
    n = len(points)
    if n == 0:
        print("No input points.")
        return

    # Generate all pair distances
    pairs = []
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i + 1, n):
            xj, yj, zj = points[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            d2 = dx*dx + dy*dy + dz*dz
            pairs.append((d2, i, j))

    # Sort by distance
    pairs.sort(key=lambda x: x[0])

    dsu = DSU(n)

    # Connect until there's 1 circuit left
    for d2, i, j in pairs:
        merged = dsu.union(i, j)
        if merged and dsu.components == 1:
            # THIS is the final needed connection
            x1 = points[i][0]
            x2 = points[j][0]
            print("Final connection between:", points[i], "and", points[j])
            print("X values:", x1, x2)
            print("Product:", x1 * x2)
            return

    print("Unexpected: did not reach 1 circuit.")

if __name__ == "__main__":
    main()
