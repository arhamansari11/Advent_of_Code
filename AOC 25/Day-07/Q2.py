
def solve():
    with open("E:\Advent of Code\AOC 25\Day-07\input.txt", 'r') as f:
        grid = [line.rstrip('\n') for line in f.readlines()]
    
    # Find the starting position 'S'
    start_row, start_col = None, None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_row, start_col = r, c
                break
        if start_row is not None:
            break
    
    # Count unique timelines using dynamic programming
    # For each position, track how many distinct paths reach it
    # When a particle hits a splitter, it takes BOTH paths (quantum superposition)
    
    from collections import defaultdict
    paths_count = defaultdict(int)
    paths_count[(start_row, start_col)] = 1
    
    # Process row by row going downward
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if paths_count[(row, col)] == 0:
                continue
            
            count = paths_count[(row, col)]
            next_row = row + 1
            
            # Check if we're at bottom
            if next_row >= len(grid):
                continue
            
            # Check what's below
            if col < len(grid[next_row]):
                next_char = grid[next_row][col]
            else:
                next_char = '.'
            
            if next_char == '^':
                # Particle encounters splitter - takes both left and right paths
                if col - 1 >= 0:
                    paths_count[(next_row, col - 1)] += count
                if col + 1 < len(grid[next_row]):
                    paths_count[(next_row, col + 1)] += count
            elif next_char == '.':
                # Empty space - particle continues downward
                paths_count[(next_row, col)] += count
    
    # Count total paths that reached the bottom row
    total = 0
    last_row = len(grid) - 1
    for col in range(len(grid[0])):
        total += paths_count[(last_row, col)]
    
    return total

answer = solve()
print(f"Answer: {answer}")