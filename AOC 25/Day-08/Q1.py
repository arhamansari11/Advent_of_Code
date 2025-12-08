



#!/usr/bin/env python3
# connect_junctions.py
# Reads points from inout.txt (one "X,Y,Z" per line), connects the 1000 closest pairs,
# then prints the product of the sizes of the three largest components.

import math
import sys
from typing import List, Tuple

# ---- Union-Find (Disjoint Set Union) ----
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def component_sizes(self) -> List[int]:
        roots = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            roots.setdefault(r, 0)
            roots[r] += 1
        return list(roots.values())

# ---- Read input ----
def read_points(filename: str) -> List[Tuple[int,int,int]]:
    pts = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                raise ValueError(f"Bad line in input: {line}")
            x,y,z = map(int, parts)
            pts.append((x,y,z))
    return pts

# ---- Main logic ----
def main():
    filename = "E:\Advent of Code\AOC 25\Day-08\input.txt"
    try:
        points = read_points(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {filename}: {e}", file=sys.stderr)
        sys.exit(1)

    n = len(points)
    if n == 0:
        print("No points found in input.")
        return

    # compute all pairwise squared distances
    pairs = []  # list of tuples (squared_dist, i, j)
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i+1, n):
            xj, yj, zj = points[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            d2 = dx*dx + dy*dy + dz*dz
            pairs.append((d2, i, j))

    # sort pairs by distance (squared)
    pairs.sort(key=lambda x: x[0])

    # take up to 1000 smallest pairs
    k = min(1000, len(pairs))
    selected = pairs[:k]

    dsu = DSU(n)
    # Connect each selected pair (union if they aren't already in same set).
    # Note: even if union returns False (already connected), the pair still counts as one of the 1000.
    for d2, i, j in selected:
        dsu.union(i, j)

    sizes = dsu.component_sizes()
    sizes.sort(reverse=True)
    # multiply top 3 sizes (if fewer than 3 components, multiply what's available; missing treated as 1)
    top3 = sizes[:3]
    while len(top3) < 3:
        top3.append(1)
    product = 1
    for s in top3:
        product *= s

    print("Number of input points:", n)
    print("Pairs considered (smallest):", k)
    print("Component sizes (descending):", sizes)
    print("Top 3 sizes:", top3)
    print("Product of top 3 sizes:", product)

if __name__ == '__main__':
    main()
