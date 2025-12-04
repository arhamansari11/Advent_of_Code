# 1.py

with open("E:\Advent of Code\AOC 25\Day-04\Input.txt") as f:
    grid = [list(line.strip()) for line in f]

rows = len(grid)
cols = len(grid[0])

dirs = [(-1,-1), (-1,0), (-1,1),
        (0,-1),          (0,1),
        (1,-1),  (1,0),  (1,1)]

count = 0

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '@':
            adj = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == '@':
                        adj += 1
            if adj < 4:
                count += 1

print(count)