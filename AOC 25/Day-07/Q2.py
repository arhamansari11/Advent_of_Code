


from collections import deque, defaultdict

# Directions
DIRS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

# How splitters work for each direction
SPLIT = {
    "/": {"U": "R", "R": "U", "D": "L", "L": "D"},
    "\\": {"U": "L", "L": "U", "D": "R", "R": "D"},
}

def part2(grid):
    R = len(grid)
    C = len(grid[0])

    start = (0, grid[0].index("S"))

    # Each beam is represented as (row, col, direction)
    # Instead of visited cells, we track visited STATES (r,c,d)
    visited = set()
    q = deque()

    # The particle "splits" in all directions from S
    for d in DIRS:
        q.append((start[0], start[1], d))
        visited.add((start[0], start[1], d))

    timelines = 0

    while q:
        r, c, d = q.popleft()
        dr, dc = DIRS[d]

        nr, nc = r + dr, c + dc

        # If out of bounds → timeline ends
        if not (0 <= nr < R and 0 <= nc < C):
            timelines += 1
            continue

        tile = grid[nr][nc]

        # Handle tile behavior
        if tile == "." or tile == "S":
            nds = [d]

        elif tile in SPLIT:
            # Mirror reflection
            nds = [SPLIT[tile][d]]

        elif tile == "|":
            if d in ("L", "R"):    # splitter: LR → U+D
                nds = ["U", "D"]
            else:                 # UD passthrough
                nds = [d]

        elif tile == "-":
            if d in ("U", "D"):    # splitter: UD → L+R
                nds = ["L", "R"]
            else:                 # LR passthrough
                nds = [d]

        else:
            nds = [d]

        # Add new states
        for nd in nds:
            state = (nr, nc, nd)
            if state not in visited:
                visited.add(state)
                q.append(state)

    return timelines


# ---- RUN ON INPUT ----

grid = [list(line.rstrip("\n")) for line in open("E:\Advent of Code\AOC 25\Day-07\input.txt")]
print(part2(grid))
