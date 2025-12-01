

# part2_safe_password.py
# Counts how many times the dial points at 0 during or at the end of each rotation.
# Dial values are 0..99 (mod 100). Start position is 50.
# Reads instructions from 'input.txt'.

def count_zero_hits(path="E:\Advent of Code\AOC 25\Day-01\input.txt"):
    pos = 50
    zero_hits = 0

    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # parse direction and distance (accepts "L68", "R 48", etc.)
            dir_char = line[0].upper()
            dist_str = line[1:].strip()
            if not dist_str or not dist_str.lstrip('-').isdigit():
                # fallback split
                parts = line.split()
                if len(parts) >= 2:
                    dir_char = parts[0][0].upper()
                    dist_str = parts[1]
                else:
                    raise ValueError(f"Can't parse instruction: {line}")
            distance = int(dist_str)
            if distance < 0:
                raise ValueError("Distance must be non-negative")

            # direction: +1 for R (increasing), -1 for L (decreasing)
            if dir_char == "R":
                s = 1
            elif dir_char == "L":
                s = -1
            else:
                raise ValueError(f"Unknown direction '{dir_char}' in line: {line}")

            # We need to count k in {1..distance} such that (pos + s*k) % 100 == 0.
            # Solve for k mod 100:
            #   if s == 1: k ≡ (100 - pos) % 100
            #   if s == -1: k ≡ pos % 100
            if distance > 0:
                if s == 1:
                    k0 = (100 - pos) % 100
                else:
                    k0 = pos % 100

                # the first positive solution within 1..100 is:
                first = k0 if k0 != 0 else 100

                if first <= distance:
                    # number of solutions = 1 + how many extra full 100-step cycles fit
                    zero_hits += 1 + (distance - first) // 100

            # update position to rotation end
            pos = (pos + s * distance) % 100

    return zero_hits


if __name__ == "__main__":
    result = count_zero_hits("E:\Advent of Code\AOC 25\Day-01\input.txt")
    print(result)
