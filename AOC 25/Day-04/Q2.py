def total_removed_rolls(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])

    # 8-directional neighbors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    def step():
        """Remove all currently accessible rolls and return how many were removed."""
        to_remove = []

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '@':
                    continue

                neighbor_rolls = 0
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '@':
                            neighbor_rolls += 1

                if neighbor_rolls < 4:
                    to_remove.append((r, c))

        # Remove them simultaneously
        for r, c in to_remove:
            grid[r][c] = '.'  # treat removed rolls as empty

        return len(to_remove)

    total_removed = 0
    while True:
        removed_this_round = step()
        if removed_this_round == 0:
            break
        total_removed += removed_this_round

    return total_removed


def main():
    # Use your specified absolute path
    file_path = "E:\Advent of Code\AOC 25\Day-04\Input.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        # Read non-empty lines as rows of the grid
        grid = [list(line.rstrip("\n")) for line in f if line.strip() != ""]

    result = total_removed_rolls(grid)
    print(result)


if __name__ == "__main__":
    main()