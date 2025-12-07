

# 2.py

with open("E:\Advent of Code\AOC 25\Day-06\input.txt", "r") as f:
    lines = [line.rstrip('\n') for line in f]

max_len = max(len(line) for line in lines)
lines = [line.ljust(max_len) for line in lines]

separator_cols = set()
for col in range(max_len):
    if all(line[col] == ' ' for line in lines):
        separator_cols.add(col)

total = 0
col = 0

while col < max_len:
    if col in separator_cols:
        col += 1
        continue

    start_col = col
    while col < max_len and col not in separator_cols:
        col += 1
    end_col = col

    op = lines[-1][start_col:end_col].strip()
    num_rows = len(lines) - 1

    numbers = []
    for c in range(end_col - 1, start_col - 1, -1):
        digits = ""
        for r in range(num_rows):
            ch = lines[r][c]
            if ch.isdigit():
                digits += ch
        if digits:
            numbers.append(int(digits))

    if not numbers or not op:
        continue

    if op == "+":
        result = sum(numbers)
    else:
        result = 1
        for n in numbers:
            result *= n

    total += result

print(total)