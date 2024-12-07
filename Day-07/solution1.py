from itertools import product

def evaluate_equation(numbers, operators):
    """
    Evaluate the equation formed by inserting the operators into the numbers list.
    """
    expression = numbers[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            expression += numbers[i + 1]
        elif operators[i] == '*':
            expression *= numbers[i + 1]
    return expression

def parse_input(file_path):
    """
    Parse the input file to extract test values and number lists.
    """
    equations = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            test_value, numbers = line.split(':')
            test_value = int(test_value.strip())
            numbers = list(map(int, numbers.strip().split()))
            equations.append((test_value, numbers))
    return equations

def find_solvable_equations(equations):
    """
    Determine which equations can be made true by inserting + or * operators.
    """
    total_calibration = 0

    for test_value, numbers in equations:
        num_positions = len(numbers) - 1
        found_solution = False

        # Generate all combinations of + and * operators for the given positions
        for ops in product(['+', '*'], repeat=num_positions):
            if evaluate_equation(numbers, ops) == test_value:
                total_calibration += test_value
                found_solution = True
                break

    return total_calibration

def main(file_path):
    equations = parse_input(file_path)
    result = find_solvable_equations(equations)
    print(f"Total Calibration Result: {result}")

if __name__ == "__main__":
    file_path = "e:/Advent of Code/Day-07/input1.txt"
    main(file_path)
