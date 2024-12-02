# Question 1 Code


# Function to check if a report is safe
def is_safe_report(report):
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    
    # Check if differences are all positive (increasing) or all negative (decreasing)
    is_increasing = all(d > 0 for d in differences)
    is_decreasing = all(d < 0 for d in differences)
    
    # Check if all differences are between 1 and 3 (inclusive)
    are_differences_valid = all(1 <= abs(d) <= 3 for d in differences)
    
    # A report is safe if it is either increasing or decreasing and the differences are valid
    return (is_increasing or is_decreasing) and are_differences_valid

# Read the input file
with open("e:/Advent of Code/Day-02/input1.txt", "r") as file:
    lines = file.read().strip().split("\n")

# Convert each line to a list of integers
reports = [list(map(int, line.split())) for line in lines]

# Check each report and count the safe ones
safe_count = sum(is_safe_report(report) for report in reports)

# Print the result
print(f"Number of safe reports: {safe_count}")
