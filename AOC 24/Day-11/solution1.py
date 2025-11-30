def process_stones(stones):
    """
    Process the list of stones according to the rules.
    """
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            half = len(str(stone)) // 2
            left = int(str(stone)[:half])
            right = int(str(stone)[half:])
            new_stones.append(left)
            new_stones.append(right)
        else:
            new_stones.append(stone * 2024)
    return new_stones


def simulate_blinks(file_path, blinks):
    """
    Simulates the blinking process for the given number of blinks.

    Parameters:
        file_path (str): Path to the input file containing initial stone numbers.
        blinks (int): Number of times to blink.

    Returns:
        int: Total number of stones after all blinks.
    """
    # Read the initial stones from the file
    with open(file_path, 'r') as file:
        stones = list(map(int, file.read().strip().split()))

    # Apply the rules for the given number of blinks
    for _ in range(blinks):
        stones = process_stones(stones)

    return len(stones)


# File path to the input
file_path = "e:/Advent of Code/Day-11/input.txt"
# Number of blinks
blinks = 25

# Calculate the total number of stones
total_stones = simulate_blinks(file_path, blinks)
print(f"Total stones after {blinks} blinks: {total_stones}")
