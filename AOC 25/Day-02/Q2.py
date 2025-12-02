# day2_giftshop_part2.py

def is_repeated_pattern(n: int) -> bool:
    s = str(n)
    L = len(s)

    # Try every possible block size
    # block must divide whole length
    for block_len in range(1, L // 2 + 1):
        if L % block_len != 0:
            continue

        block = s[:block_len]
        repeats = L // block_len

        if repeats >= 2 and block * repeats == s:
            return True

    return False


def sum_invalid_ids_part2(path="E:\Advent of Code\AOC 25\Day-02\input.txt"):
    with open(path, "r") as f:
        line = f.read().strip()

    total = 0

    # Split ranges by commas
    for r in line.split(","):
        r = r.strip()
        if not r:
            continue

        lo, hi = r.split("-")
        lo, hi = int(lo), int(hi)

        for x in range(lo, hi + 1):
            if is_repeated_pattern(x):
                total += x

    return total


if __name__ == "__main__":
    print(sum_invalid_ids_part2("E:\Advent of Code\AOC 25\Day-02\input.txt"))
