


# day3_lobby_part2.py

def max_number_from_digits(s: str, k: int) -> int:
    """
    Given a string s of digits, pick exactly k digits in order
    to form the largest possible number.
    """
    stack = []
    drop = len(s) - k  # number of digits we can remove

    for digit in s:
        while drop and stack and stack[-1] < digit:
            stack.pop()
            drop -= 1
        stack.append(digit)

    # In case we didn't drop enough, trim from the end
    result_digits = stack[:k]
    return int("".join(result_digits))


def total_max_joltage_12(path="E:\Advent of Code\AOC 25\Day-03\Input.txt") -> int:
    total = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                total += max_number_from_digits(line, 12)
    return total


if __name__ == "__main__":
    print(total_max_joltage_12("E:\Advent of Code\AOC 25\Day-03\Input.txt"))
