
from collections import defaultdict, Counter

def count_paths_fast(graph, start, end, required=None):
    """Ultra-fast iterative DFS with path counting and memoization"""
    if required is None:
        required = set()
    
    # DP: (node, required_mask) -> path count to end
    memo = {}
    
    def dp(node, mask):
        if node == end:
            return 1 if mask == (1 << len(required)) - 1 else 0
        
        key = (node, mask)
        if key in memo:
            return memo[key]
        
        count = 0
        visited = set()
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_mask = mask
                if neighbor in required:
                    req_idx = list(required).index(neighbor)
                    new_mask |= (1 << req_idx)
                count += dp(neighbor, new_mask)
        
        memo[key] = count
        return count
    
    return dp(start, 0)

# Build graph
graph = defaultdict(list)
with open('E:\Advent of Code\AOC 25\Day-11\input.txt', 'r') as f:
    for line in f:
        if ':' in line:
            device, outputs = line.strip().split(':', 1)
            graph[device.strip()].extend(output.strip() for output in outputs.split() if output.strip())

# PART 1: Paths from 'you' to 'out' 
part1 = count_paths_fast(graph, 'you', 'out')

# PART 2: Paths from 'svr' to 'out' visiting both 'dac' and 'fft'
required = {'dac', 'fft'}
part2 = count_paths_fast(graph, 'svr', 'out', required)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")

with open('output.txt', 'w') as f:
    f.write(f"{part1}\n{part2}")