
from itertools import combinations
import re
import z3


def parse_input(text):
    machines = []

    for line in text.strip().splitlines():
        parts = line.split()

        # lights
        light_str = parts[0][1:-1]
        lights = [c == "#" for c in light_str]

        # everything between lights and joltages are buttons
        button_parts = parts[1:-1]
        buttons = []
        for bp in button_parts:
            buttons.append([int(x) for x in re.findall(r"\d+", bp)])

        # last part is joltages
        joltages = [int(x) for x in re.findall(r"\d+", parts[-1])]

        machines.append((lights, buttons, joltages))

    return machines


# -------------------------
# PART 1
# -------------------------
def solve_part1(machines):
    total = 0

    for lights, buttons, _ in machines:
        if not any(lights):
            continue

        # brute-force increasing number of presses
        for presses in range(1, 25):  # enough for AoC input
            for combo in combinations(buttons, presses):
                test = [False] * len(lights)
                for btn in combo:
                    for pos in btn:
                        test[pos % len(test)] = not test[pos % len(test)]
                if test == lights:
                    total += presses
                    break
            else:
                continue
            break

    return total


# -------------------------
# PART 2
# -------------------------
def solve_part2(machines):
    total = 0

    for _, buttons, target in machines:
        solver = z3.Optimize()
        vars = [z3.Int(f"x{i}") for i in range(len(buttons))]

        # x[j] ≥ 0
        for v in vars:
            solver.add(v >= 0)

        # Build the equation A*x = target
        counter_eq = [0] * len(target)
        for j, btn in enumerate(buttons):
            for pos in btn:
                if 0 <= pos < len(target):
                    counter_eq[pos] += vars[j]

        # Add constraints
        for i in range(len(target)):
            solver.add(counter_eq[i] == target[i])

        # Minimize total presses
        solver.minimize(sum(vars))

        if solver.check() == z3.sat:
            model = solver.model()
            presses = sum(model[v].as_long() for v in vars)
            total += presses
        else:
            raise RuntimeError("No solution found (should never happen).")

    return total


# -------------------------
# RUN EVERYTHING
# -------------------------
def main():
    with open("E:\Advent of Code\AOC 25\Day-10\input.txt", "r") as f:
        text = f.read()

    machines = parse_input(text)

    part1 = solve_part1(machines)
    part2 = solve_part2(machines)

    with open("output.txt", "w") as f:
        f.write(str(part1) + "\n" + str(part2))


if __name__ == "__main__":
    main()