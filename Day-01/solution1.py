# Question 1 Code


# # Read the input file
with open("e:/Advent of Code/Day-1/input.txt") as f:
    lines = f.read().strip().split("\n")

# Parse the input into two separate lists
left = []
right = []

for line in lines:
    l, r = map(int, line.split())  # Split each line into two numbers
    left.append(l)                # Add to left list
    right.append(r)               # Add to right list

# Sort both lists
left.sort()
right.sort()

# Calculate the total distance
total_distance = sum(abs(l - r) for l, r in zip(left, right))

# Print the result
print("Total distance:", total_distance)
