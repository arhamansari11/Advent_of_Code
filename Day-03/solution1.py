import re

def sum_valid_multiplications(file_path):
    # Read the input file
    with open(file_path, "r") as f:
        data = f.read()
    
    # Regex to match valid mul instructions (e.g., mul(123,456))
    valid_mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
    
    # Find all matches in the input
    matches = re.findall(valid_mul_pattern, data)
    
    total_sum = 0
    for match in matches:
        # Extract numbers from the valid mul instruction
        numbers = list(map(int, re.findall(r"\d+", match)))
        # Multiply and add to total sum
        total_sum += numbers[0] * numbers[1]
    
    return total_sum

# File path to the input file
file_path = "e:/Advent of Code/Day-03/input1.txt"

# Call the function and print the result
result = sum_valid_multiplications(file_path)
print("Total sum of valid multiplications:", result)
