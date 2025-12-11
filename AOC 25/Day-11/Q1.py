
from collections import defaultdict, deque

def count_paths(graph, start, end):
    """Count all paths from start to end using DFS with memoization"""
    def dfs(node, visited):
        if node == end:
            return 1
        
        visited.add(node)
        count = 0
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                count += dfs(neighbor, visited.copy())
        
        visited.remove(node)
        return count
    
    return dfs(start, set())

# Build graph
graph = defaultdict(list)
with open('E:\Advent of Code\AOC 25\Day-11\input.txt', 'r') as f:
    for line in f:
        if ':' in line:
            device, outputs = line.strip().split(':', 1)
            graph[device.strip()].extend(output.strip() for output in outputs.split())

# Count paths from 'you' to 'out'
path_count = count_paths(graph, 'you', 'out')

with open('output.txt', 'w') as f:
    f.write(str(path_count))

print(f"Number of paths from 'you' to 'out': {path_count}")
