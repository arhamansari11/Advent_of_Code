def count_x_mas(grid):
    rows = len(grid)
    cols = len(grid[0])
    total_count = 0

    # Check if a given position forms an X-MAS
    def is_x_mas(r, c):
        # Ensure the position is within bounds
        if r - 1 < 0 or r + 1 >= rows or c - 1 < 0 or c + 1 >= cols:
            return False

        # Extract characters forming the X
        tl_br = [grid[r - 1][c - 1], grid[r][c], grid[r + 1][c + 1]]  # Top-left to bottom-right
        tr_bl = [grid[r - 1][c + 1], grid[r][c], grid[r + 1][c - 1]]  # Top-right to bottom-left

        # Check all valid "MAS" configurations
        valid_mas = {"MAS", "SAM"}
        return (''.join(tl_br) in valid_mas and ''.join(tr_bl) in valid_mas)

    # Iterate through each cell as a potential center
    for r in range(rows):
        for c in range(cols):
            if is_x_mas(r, c):
                total_count += 1

    return total_count

# File path to the input file
file_path = "e:/Advent of Code/Day-04/input2.txt"

# Read the grid from the file
with open(file_path, "r") as file:
    grid = [line.strip() for line in file.readlines()]

# Debug: Print the grid to confirm it is read correctly
print("Grid Read from File:")
print("\n".join(grid))

# Count all occurrences of X-MAS
x_mas_count = count_x_mas(grid)

# Output the result
print(f"Total occurrences of 'X-MAS': {x_mas_count}")
