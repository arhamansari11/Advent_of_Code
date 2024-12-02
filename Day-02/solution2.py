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

# Function to check if removing one level makes the report safe
def can_be_safe_with_removal(report):
    n = len(report)
    for i in range(n):
        # Create a new report by removing the i-th level
        modified_report = report[:i] + report[i+1:]
        # Check if the modified report is safe
        if is_safe_report(modified_report):
            return True
    return False

# Read the input file
with open("e:/Advent of Code/Day-02/input2.txt", "r") as file:
    lines = file.read().strip().split("\n")

# Convert each line to a list of integers
reports = [list(map(int, line.split())) for line in lines]

# Check each report and count the safe ones, including those made safe by the Problem Dampener
safe_count = 0
for report in reports:
    if is_safe_report(report) or can_be_safe_with_removal(report):
        safe_count += 1

# Print the result
print(f"Number of safe reports with Problem Dampener: {safe_count}")
