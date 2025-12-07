# 1.py
def solve():
    grid = [list(line.rstrip('\n')) for line in open("E:\Advent of Code\AOC 25\Day-07\input.txt")]
    R, C = len(grid), len(grid[0])

    # find S
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = (r, c)

    # beams are (r, c)
    beams = [(start[0], start[1])]
    visited = set()
    splits = 0

    while beams:
        new_beams = []
        for r, c in beams:
            nr = r + 1
            if nr >= R:
                continue
            cell = grid[nr][c]

            if cell == '.':
                if (nr, c) not in visited:
                    visited.add((nr, c))
                    new_beams.append((nr, c))

            elif cell == '^':
                splits += 1
                # left
                if c - 1 >= 0 and (nr, c - 1) not in visited:
                    visited.add((nr, c - 1))
                    new_beams.append((nr, c - 1))
                # right
                if c + 1 < C and (nr, c + 1) not in visited:
                    visited.add((nr, c + 1))
                    new_beams.append((nr, c + 1))

            # S itself should be treated as empty when beams pass below it
            elif cell == 'S':
                if (nr, c) not in visited:
                    visited.add((nr, c))
                    new_beams.append((nr, c))

        beams = new_beams

    print(splits)

if __name__ == "__main__":
    solve()