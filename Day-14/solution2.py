import re
from collections import defaultdict

# Define grid dimensions
GRID_WIDTH = 101
GRID_HEIGHT = 103

# Define the function to parse input
def parse_input(input_file):
    robots = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip())
            if match:
                px, py, vx, vy = map(int, match.groups())
                robots.append(((px, py), (vx, vy)))
    return robots

# Simulate robots
def simulate_robots(robots, seconds):
    positions = defaultdict(int)

    for (px, py), (vx, vy) in robots:
        # Calculate new position after 'seconds' time steps with wrapping
        nx = (px + vx * seconds) % GRID_WIDTH
        ny = (py + vy * seconds) % GRID_HEIGHT
        positions[(nx, ny)] += 1

    return positions

# Render the grid for visualization
def render_grid(positions):
    grid = [["." for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    for (x, y), count in positions.items():
        grid[y][x] = "#" if count > 0 else "."

    return "\n".join("".join(row) for row in grid)

# Find the time step where robots align
def find_alignment_time(robots):
    for seconds in range(10000):  # Arbitrary upper limit to avoid infinite loops
        positions = simulate_robots(robots, seconds)

        # Check if the positions form a condensed pattern
        x_coords = [x for (x, y) in positions.keys()]
        y_coords = [y for (x, y) in positions.keys()]

        if max(x_coords) - min(x_coords) < 20 and max(y_coords) - min(y_coords) < 20:
            print(f"Pattern detected at {seconds} seconds:")
            print(render_grid(positions))
            return seconds

    return -1  # Return -1 if no pattern is found

if __name__ == "__main__":
    input_file = "e:/Advent of Code/Day-14/input.txt"

    # Parse input
    robots = parse_input(input_file)

    # Find alignment time
    alignment_time = find_alignment_time(robots)

    if alignment_time != -1:
        print(f"Fewest number of seconds for alignment: {alignment_time}")
    else:
        print("No alignment found within the time limit.")
