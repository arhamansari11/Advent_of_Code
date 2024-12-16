from collections import defaultdict

# Read input from 'input.txt'
with open("e:/Advent of Code/Day-15/input.txt", 'r') as f:
    inp = f.read()

# Split the input into grid and directions
parts = inp.split("\n\n")
lines = parts[0].split("\n")

# Function to expand grid tiles
def expand(c):
    if c == "O":
        return "[]"
    elif c == "@":
        return "@."
    else:
        return c + c

# Expanding the grid
lines = ["".join(expand(c) for c in l) for l in lines]
print("\n".join(lines))

# Dimensions of the expanded grid
m = len(lines)
n = len(lines[0])

# Create a grid (using defaultdict to simplify handling of missing cells)
grid = defaultdict(lambda: defaultdict(lambda: "!"))
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        grid[i][j] = c

# Directions corresponding to <, >, ^, v
dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]
chardirs = {"<": 1, ">": 0, "^": 2, "v": 3}

# Function to check if a move is valid
def check_move(d, i, j, already_checked):
    if (i, j) in already_checked:
        return already_checked[(i, j)]
    already_checked[(i, j)] = True
    if grid[i][j] == "#":
        already_checked[(i, j)] = False
    elif grid[i][j] == ".":
        already_checked[(i, j)] = True
    elif grid[i][j] == "@":
        already_checked[(i, j)] = check_move(d, i + d[0], j + d[1], already_checked)
    elif grid[i][j] == "[":
        already_checked[(i, j)] = check_move(d, i + d[0], j + d[1], already_checked) and check_move(d, i, j + 1, already_checked)
    elif grid[i][j] == "]":
        already_checked[(i, j)] = check_move(d, i + d[0], j + d[1], already_checked) and check_move(d, i, j - 1, already_checked)
    return already_checked[(i, j)]

# Function to commit the move
def commit_move(d, i, j, already_committed):
    if (i, j) in already_committed:
        return
    already_committed.add((i, j))
    if grid[i][j] == "#":
        return
    elif grid[i][j] == ".":
        return
    elif grid[i][j] == "[":
        commit_move(d, i + d[0], j + d[1], already_committed)
        commit_move(d, i, j + 1, already_committed)
        grid[i + d[0]][j + d[1]] = grid[i][j]
        grid[i][j] = "."
    elif grid[i][j] == "]":
        commit_move(d, i + d[0], j + d[1], already_committed)
        commit_move(d, i, j - 1, already_committed)
        grid[i + d[0]][j + d[1]] = grid[i][j]
        grid[i][j] = "."
    elif grid[i][j] == "@":
        commit_move(d, i + d[0], j + d[1], already_committed)
        grid[i + d[0]][j + d[1]] = grid[i][j]
        grid[i][j] = "."

# Find initial robot position
robot_pos = (0, 0)
for i in range(m):
    for j in range(n):
        if grid[i][j] == "@":
            robot_pos = (i, j)

# Directions to move (from input)
for dirchar in parts[1]:
    if dirchar == "\n":
        continue
    d = dirs[chardirs[dirchar]]  # Get the direction tuple
    if check_move(d, robot_pos[0], robot_pos[1], {}):
        commit_move(d, robot_pos[0], robot_pos[1], set())  # Commit the move
        robot_pos = (robot_pos[0] + d[0], robot_pos[1] + d[1])  # Update robot position

# Calculate GPS sum for boxes
result = 0
for i in range(m):
    for j in range(n):
        if grid[i][j] == "[":
            # Calculate the GPS coordinate for the box
            result += 100 * i + j

# Print the final result
print("Final GPS sum:", result)