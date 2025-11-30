def read_input(file_path):
    """Reads the input file and returns the topographic map as a list of lists."""
    with open(file_path, 'r') as f:
        return [list(map(int, line.strip())) for line in f.readlines()]

def find_trailheads(topographic_map):
    """Find all trailhead positions in the map (positions with height 0)."""
    trailheads = []
    for i in range(len(topographic_map)):
        for j in range(len(topographic_map[0])):
            if topographic_map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def dfs(map_, visited, x, y):
    """Perform depth-first search to find hiking trails starting from a given position."""
    stack = [(x, y, 0)]  # (current_x, current_y, current_height)
    reachable_nines = set()

    while stack:
        cx, cy, height = stack.pop()
        
        # Check bounds
        if cx < 0 or cx >= len(map_) or cy < 0 or cy >= len(map_[0]):
            continue
        
        # Check if already visited or height is invalid
        if visited[cx][cy] or map_[cx][cy] != height:
            continue

        visited[cx][cy] = True

        # If we reach height 9, mark it
        if map_[cx][cy] == 9:
            reachable_nines.add((cx, cy))

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            stack.append((cx + dx, cy + dy, height + 1))

    return len(reachable_nines)

def calculate_total_score(map_):
    """Calculate the total score of all trailheads."""
    trailheads = find_trailheads(map_)
    total_score = 0

    for trailhead in trailheads:
        visited = [[False for _ in range(len(map_[0]))] for _ in range(len(map_))]
        score = dfs(map_, visited, trailhead[0], trailhead[1])
        total_score += score

    return total_score

def main():
    fn = "e:/Advent of Code/Day-10/input.txt"
    topographic_map = read_input(fn)
    total_score = calculate_total_score(topographic_map)
    print(f"Total score of all trailheads: {total_score}")

if __name__ == "__main__":
    main()
