
from collections import defaultdict, deque
def parse_input(file_path):
    with open(file_path, "r") as file:
        sections = file.read().strip().split("\n\n")
        rules = [tuple(map(int, line.split("|"))) for line in sections[0].split("\n")]
        updates = [list(map(int, line.split(","))) for line in sections[1].split("\n")]
    return rules, updates
def validate_update(update, precedence_rules):
    for x, y in precedence_rules:
        if x in update and y in update:
            if update.index(x) > update.index(y):
                return False
    return True
def build_graph(precedence_rules):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for x, y in precedence_rules:
        graph[x].append(y)
        in_degree[y] += 1
        in_degree.setdefault(x, 0)  # Ensure all nodes appear in in_degree
    return graph, in_degree
def topological_sort(update, graph, in_degree):
    # Only consider nodes present in the update
    filtered_graph = {node: [] for node in update}
    filtered_in_degree = {node: 0 for node in update}
    for node in update:
        for neighbor in graph[node]:
            if neighbor in update:
                filtered_graph[node].append(neighbor)
                filtered_in_degree[neighbor] += 1
    # Perform topological sort
    queue = deque([node for node in update if filtered_in_degree[node] == 0])
    sorted_update = []
    while queue:
        node = queue.popleft()
        sorted_update.append(node)
        for neighbor in filtered_graph[node]:
            filtered_in_degree[neighbor] -= 1
            if filtered_in_degree[neighbor] == 0:
                queue.append(neighbor)
    return sorted_update
def fix_and_find_middle_sum(file_path):
    rules, updates = parse_input(file_path)
    graph, in_degree = build_graph(rules)
    incorrect_updates = []
    fixed_updates_middle_sum = 0
    for update in updates:
        if validate_update(update, rules):
            continue  # Skip correctly-ordered updates
        incorrect_updates.append(update)
        sorted_update = topological_sort(update, graph, in_degree)
        middle_page = sorted_update[len(sorted_update) // 2]
        fixed_updates_middle_sum += middle_page
    return fixed_updates_middle_sum
# File path to the input data
file_path =  "e:/Advent of Code/Day-05/input2.txt"
# Find and print the sum of middle pages for fixed updates
result = fix_and_find_middle_sum(file_path)
print(f"Sum of middle page numbers from fixed updates: {result}")