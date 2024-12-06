def read_map(file_path):
    with open(file_path, 'r') as file:
        return [list(line.strip()) for line in file]

def guard_patrol(grid):
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    direction_order = ['^', '>', 'v', '<']

    # Find the guard's starting position and facing direction
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in directions:
                guard_pos = (r, c)
                guard_dir = cell
                break

    visited = set()
    rows, cols = len(grid), len(grid[0])

    while 0 <= guard_pos[0] < rows and 0 <= guard_pos[1] < cols:
        visited.add(guard_pos)

        dr, dc = directions[guard_dir]
        next_pos = (guard_pos[0] + dr, guard_pos[1] + dc)

        if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and grid[next_pos[0]][next_pos[1]] == '#':
            # Turn right 90 degrees
            guard_dir = direction_order[(direction_order.index(guard_dir) + 1) % 4]
        else:
            # Move forward
            guard_pos = next_pos

    return visited

def mark_visited(grid, visited):
    for r, c in visited:
        if grid[r][c] == '.':
            grid[r][c] = 'X'

def main(file_path):
    grid = read_map(file_path)
    visited = guard_patrol(grid)
    mark_visited(grid, visited)

    # Print the grid with the marked path
    for row in grid:
        print(''.join(row))

    print("Distinct positions visited:", len(visited))

if __name__ == "__main__":
    file_path = "e:/Advent of Code/Day-06/input1.txt"
    main(file_path)
