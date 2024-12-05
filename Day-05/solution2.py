import re

def sum_enabled_multiplications(file_path):
    # Read the input file
    with open(file_path, "r") as f:
        data = f.read()
    
    # Regex to match valid mul instructions and control instructions
    valid_mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    
    # Split the input into tokens based on instructions
    tokens = re.split(r"(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))", data)
    
    # Initialize variables
    mul_enabled = True  # Multiplications are enabled at the start
    total_sum = 0

    for token in tokens:
        token = token.strip()
        if token == "do()":
            # Enable mul instructions
            mul_enabled = True
        elif token == "don't()":
            # Disable mul instructions
            mul_enabled = False
        elif re.match(valid_mul_pattern, token) and mul_enabled:
            # Process valid mul instructions if enabled
            numbers = list(map(int, re.findall(r"\d+", token)))
            total_sum += numbers[0] * numbers[1]
    
    return total_sum

# File path to the input file
file_path = "e:/Advent of Code/Day-03/input2.txt"

# Call the function and print the result
result = sum_enabled_multiplications(file_path)
print("Total sum of enabled multiplications:", result)
