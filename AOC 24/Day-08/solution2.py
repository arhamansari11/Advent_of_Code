def find_all_antinodes(file_path):
    from collections import defaultdict
    # Step 1: Read the input file and parse the grid
    with open(file_path, 'r') as file:
        grid = [line.strip() for line in file.readlines()]
    # Parse grid to collect antenna positions by frequency
    antenna_positions = defaultdict(list)
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            char = grid[r][c]
            if char.isalnum():  # Antennas are letters or digits
                antenna_positions[char].append((r, c))
    # Step 2: Find all antinodes for each frequency
    unique_antinodes = set()
    for freq, positions in antenna_positions.items():
        n = len(positions)
        if n < 2:
            continue  # No antinodes possible with fewer than 2 antennas
        # Add all antenna positions as antinodes
        unique_antinodes.update(positions)
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # Compute direction vector
                dr = r2 - r1
                dc = c2 - c1
                # Generate all points along the line
                for k in range(-max(rows, cols), max(rows, cols) + 1):
                    r_antin = r1 + k * dr
                    c_antin = c1 + k * dc
                    # Add valid antinodes within bounds
                    if 0 <= r_antin < rows and 0 <= c_antin < cols:
                        unique_antinodes.add((r_antin, c_antin))
    # Step 3: Return the count of unique antinodes
    return len(unique_antinodes)

# Path to the input files
file_path = "e:/Advent of Code/Day-08/input.txt"


# Call the function and print the result
unique_count = find_all_antinodes(file_path)
print(f"Number of unique antinode locations: {unique_count}")