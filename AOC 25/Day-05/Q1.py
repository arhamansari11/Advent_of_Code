

# day5_cafeteria_part1.py

def count_fresh_ingredients(path="E:\Advent of Code\AOC 25\Day-05\input.txt") -> int:
    ranges = []
    available_ids = []
    reading_ranges = True

    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "":
                reading_ranges = False
                continue

            if reading_ranges:
                start, end = map(int, line.split("-"))
                ranges.append((start, end))
            else:
                available_ids.append(int(line))

    fresh_count = 0
    for ingredient in available_ids:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh_count += 1
                break   # no need to check more ranges

    return fresh_count


if __name__ == "__main__":
    print(count_fresh_ingredients("E:\Advent of Code\AOC 25\Day-05\input.txt"))
