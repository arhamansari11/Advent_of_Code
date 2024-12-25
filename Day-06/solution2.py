import sys
from collections import defaultdict, Counter, deque

# Set the recursion limit (this is rarely needed but might be helpful for large datasets)
sys.setrecursionlimit(10**6)

# Path to the input file
infile =  "e:/Advent of Code/Day-06/input2.txt"  # Path to input.txt file

# Initialize variables for part 1 and part 2 answers
p1 = 0
p2 = 0

# Read the entire input file and split it into lines
with open(infile, 'r') as file:
    D = file.read().strip()

# Split the input into grid G
G = D.split('\n')
R = len(G)
C = len(G[0])

# Find the starting position of the guard ('^')
for r in range(R):
    for c in range(C):
        if G[r][c] == '^':
            sr, sc = r, c

# Simulate the guard's movement for part 1 and part 2
for o_r in range(R):
    for o_c in range(C):
        r, c = sr, sc
        d = 0  # 0=up, 1=right, 2=down, 3=left
        SEEN = set()
        SEEN_RC = set()

        while True:
            if (r, c, d) in SEEN:
                p2 += 1
                break
            SEEN.add((r, c, d))
            SEEN_RC.add((r, c))
            dr, dc = [(-1, 0), (0, 1), (1, 0), (0, -1)][d]
            rr = r + dr
            cc = c + dc

            # Check if the new position is out of bounds
            if not (0 <= rr < R and 0 <= cc < C):
                if G[o_r][o_c] == '#':
                    p1 = len(SEEN_RC)  # Number of distinct positions visited
                break

            # If the guard encounters an obstacle, it turns right (90 degrees)
            if G[rr][cc] == '#' or (rr == o_r and cc == o_c):
                d = (d + 1) % 4
            else:
                r = rr
                c = cc

# Output the results for part 1 and part 2
print(f"Part 1 result: {p1}")  # Part 1 result
print(f"Part 2 result: {p2}")  # Part 2 result