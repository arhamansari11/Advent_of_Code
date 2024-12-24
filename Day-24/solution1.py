from collections import defaultdict
import re
from itertools import permutations

# Read input from file
def read_input(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip().split('\n')

# Perform logic gate operations
def apply_gate(gate, a, b):
    if gate == 'AND':
        return a & b
    elif gate == 'OR':
        return a | b
    elif gate == 'XOR':
        return a ^ b
    return None

# Simulate the circuit
def simulate_circuit(lines, swaps=None):
    wire_values = {}
    gate_operations = []

    # Parse input
    for line in lines:
        if ':' in line:
            wire, value = line.split(': ')
            wire_values[wire] = int(value)
        else:
            gate_operations.append(line)

    if swaps:
        # Apply swaps
        for a, b in swaps:
            gate_operations = [
                re.sub(f'\b{a}\b', 'TEMP', op)
                .replace(b, a)
                .replace('TEMP', b)
                for op in gate_operations
            ]

    # Process gates until all outputs are computed
    while gate_operations:
        remaining_operations = []
        for operation in gate_operations:
            match = re.match(r'(.+) (AND|OR|XOR) (.+) -> (.+)', operation)
            if match:
                a, gate, b, output = match.groups()
                if a in wire_values and b in wire_values:
                    wire_values[output] = apply_gate(gate, wire_values[a], wire_values[b])
                else:
                    remaining_operations.append(operation)
        gate_operations = remaining_operations

    # Collect and sort output wires starting with 'z'
    output_bits = []
    for wire, value in wire_values.items():
        if wire.startswith('z'):
            output_bits.append((wire, value))

    output_bits.sort()  # Sort to ensure correct binary order (z00, z01, ...)

    # Construct binary output
    binary_result = ''.join(str(bit[1]) for bit in output_bits[::-1])
    return int(binary_result, 2), wire_values

# Find swapped wires
def find_swapped_wires(lines):
    all_wires = set(re.findall(r'\b[a-z]+[0-9]+\b', ' '.join(lines)))
    z_wires = sorted(w for w in all_wires if w.startswith('z'))
    
    # Generate all possible pairs of swaps (4 pairs -> 8 wires)
    possible_swaps = list(permutations(z_wires, 2))

    for swap_set in permutations(possible_swaps, 4):
        # Ensure no wire is swapped more than once
        swapped_wires = {wire for pair in swap_set for wire in pair}
        if len(swapped_wires) != 8:
            continue

        # Simulate circuit with current swap configuration
        result, wire_values = simulate_circuit(lines, swaps=swap_set)
        
        # Validate result (correct addition output)
        x_value = int(''.join(str(wire_values[f'x{str(i).zfill(2)}']) for i in range(len(z_wires))), 2)
        y_value = int(''.join(str(wire_values[f'y{str(i).zfill(2)}']) for i in range(len(z_wires))), 2)
        if result == x_value + y_value:
            return sorted(swapped_wires)

if __name__ == "__main__":
    input_lines = read_input("e:/Advent of Code/Day-24/input.txt")
    swapped_wires = find_swapped_wires(input_lines)
    print("Swapped Wires:", ','.join(swapped_wires))