from collections import deque

def parse_input(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f]

def find_start_end(grid):
    start = end = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
            elif cell == 'E':
                end = (r, c)
    return start, end

def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    direction_names = ['N', 'S', 'W', 'E']
    
    # Queue stores (row, col, direction, score)
    queue = deque([(start[0], start[1], 3, 0)])  # Start facing East (index 3)
    visited = set()
    visited.add((start[0], start[1], 3))

    while queue:
        r, c, direction, score = queue.popleft()

        # If we reach the end, return the score
        if (r, c) == end:
            return score

        # Explore all possible movements
        for i, (dr, dc) in enumerate(directions):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                new_direction = i
                turn_cost = 1000 if new_direction != direction else 0
                new_score = score + 1 + turn_cost
                state = (nr, nc, new_direction)

                if state not in visited:
                    visited.add(state)
                    queue.append((nr, nc, new_direction, new_score))

    return float('inf')  # If no path is found

def main():
    input_data = parse_input("e:/Advent of Code/Day-16/input.txt")
    start, end = find_start_end(input_data)
    lowest_score = bfs(input_data, start, end)
    print(f"The lowest score a Reindeer could possibly get: {lowest_score}")

if __name__ == "__main__":
    main()
