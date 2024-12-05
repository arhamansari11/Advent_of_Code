from collections import defaultdict, deque

# Function to parse the input file
def parse_input(file_path):
    with open(file_path, 'r') as file:
        sections = file.read().strip().split("\n\n")
        
        # First section contains the rules
        rules = [tuple(map(int, line.split('|'))) for line in sections[0].splitlines()]
        
        # Second section contains the updates
        updates = [list(map(int, line.split(','))) for line in sections[1].splitlines()]
        
        return rules, updates

# Function to check if an update is in the correct order
def is_correct_order(update, rules):
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            # Ensure that rule[0] appears before rule[1] in the update
            if update.index(rule[0]) > update.index(rule[1]):
                return False
    return True

# Function to fix the order of a single update
def fix_order(update, rules):
    # Build a graph of dependencies
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            graph[rule[0]].append(rule[1])
            in_degree[rule[1]] += 1
            if rule[0] not in in_degree:
                in_degree[rule[0]] = 0

    # Perform a topological sort
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_update = []
    while queue:
        node = queue.popleft()
        sorted_update.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Return the sorted update based on the topological order
    return sorted_update

# Function to process incorrectly ordered updates and compute the sum of their middle pages
def sum_of_fixed_middle_pages(file_path):
    rules, updates = parse_input(file_path)
    
    middle_pages_sum = 0
    for update in updates:
        if not is_correct_order(update, rules):
            # Fix the order of the update
            fixed_update = fix_order(update, rules)
            # Find the middle page number
            middle_page = fixed_update[len(fixed_update) // 2]
            middle_pages_sum += middle_page

    return middle_pages_sum

# File path to the input file
file_path = "e:/Advent of Code/Day-05/input2.txt"

# Calculate the result
result = sum_of_fixed_middle_pages(file_path)
print(f"The sum of the middle page numbers after fixing is: {result}")
