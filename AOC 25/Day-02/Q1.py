# day2_giftshop.py

def is_repeated_twice(n: int) -> bool:
    s = str(n)
    length = len(s)

    # Must have even length
    if length % 2 != 0:
        return False

    half = length // 2
    return s[:half] == s[half:]


def sum_invalid_ids(path="E:\Advent of Code\AOC 25\Day-02\input.txt"):
    with open(path, "r") as f:
        line = f.read().strip()

    total = 0

    # Split ranges by commas
    ranges = line.split(",")

    for r in ranges:
        if not r.strip():
            continue
        lo, hi = r.split("-")
        lo, hi = int(lo), int(hi)

        for x in range(lo, hi + 1):
            if is_repeated_twice(x):
                total += x

    return total


if __name__ == "__main__":
    print(sum_invalid_ids("E:\Advent of Code\AOC 25\Day-02\input.txt"))
