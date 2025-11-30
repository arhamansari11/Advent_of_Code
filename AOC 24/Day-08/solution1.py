def find_unique_antinodes_from_file(file_path):
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
    # Step 2: Find antinodes for each frequency
    unique_antinodes = set()
    for freq, positions in antenna_positions.items():
        n = len(positions)
        if n < 2:
            continue  # No antinodes possible with fewer than 2 antennas
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # Compute differences
                dr = r2 - r1
                dc = c2 - c1
                # First antinode (closer to r1, c1)
                r_antin1, c_antin1 = r1 - dr, c1 - dc
                # Second antinode (further from r2, c2)
                r_antin2, c_antin2 = r2 + dr, c2 + dc
                # Add valid antinodes within bounds
                if 0 <= r_antin1 < rows and 0 <= c_antin1 < cols:
                    unique_antinodes.add((r_antin1, c_antin1))
                if 0 <= r_antin2 < rows and 0 <= c_antin2 < cols:
                    unique_antinodes.add((r_antin2, c_antin2))
    # Step 3: Return the count of unique antinodes
    return len(unique_antinodes)
# Path to the input file
file_path = "e:/Advent of Code/Day-08/input.txt"
# Call the function and print the result
unique_count = find_unique_antinodes_from_file(file_path)
print(f"Number of unique antinode locations: {unique_count}")