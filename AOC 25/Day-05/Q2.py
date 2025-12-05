


# day5_cafeteria_part2.py

def count_all_fresh_ids(path="E:\Advent of Code\AOC 25\Day-05\input.txt") -> int:
    ranges = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "":
                break  # stop at blank line
            start, end = map(int, line.split("-"))
            ranges.append((start, end))

    # Sort ranges by start
    ranges.sort()

    # Merge overlapping intervals
    merged = []
    for start, end in ranges:
        if not merged or start > merged[-1][1] + 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    # Count total number of fresh IDs
    total = sum(end - start + 1 for start, end in merged)
    return total


if __name__ == "__main__":
    print(count_all_fresh_ids("E:\Advent of Code\AOC 25\Day-05\input.txt"))
