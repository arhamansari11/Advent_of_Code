# Read two-column input from a text file and compute total distance
"E:\Advent of Code\AOC 25\Day-01\input.txt"


# safe_password.py
# Reads rotation instructions from 'input.txt' and prints how many times
# the dial points at 0 after any rotation. Dial values are 0..99 (mod 100).
# Starts at 50.

def count_zeros_from_file(path="E:\Advent of Code\AOC 25\Day-01\input.txt"):
    pos = 50           # starting position
    zeros = 0

    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            # Accept forms like "L68", "R 48", "L  30", etc.
            dir_char = line[0].upper()
            dist_str = line[1:].strip()
            if not dist_str.isdigit():
                # try splitting on whitespace if first-char parsing fails
                parts = line.split()
                if len(parts) >= 2:
                    dir_char = parts[0][0].upper()
                    dist_str = parts[1]
                else:
                    raise ValueError(f"Can't parse instruction: {line}")
            distance = int(dist_str)

            if dir_char == "L":
                pos = (pos - distance) % 100
            elif dir_char == "R":
                pos = (pos + distance) % 100
            else:
                raise ValueError(f"Unknown direction '{dir_char}' in line: {line}")

            if pos == 0:
                zeros += 1

    return zeros

if __name__ == "__main__":
    result = count_zeros_from_file("E:\Advent of Code\AOC 25\Day-01\input.txt")
    print(result)
