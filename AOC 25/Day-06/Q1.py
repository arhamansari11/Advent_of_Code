# 1.py
import re

with open("E:\Advent of Code\AOC 25\Day-06\input.txt", "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f]

if not lines:
    print(0)
    exit()

maxlen = max(len(line) for line in lines)
# build char matrix padded with spaces
matrix = [list(line.ljust(maxlen)) for line in lines]
rows = len(matrix)
cols = maxlen

# find contiguous non-empty column blocks (problems)
blocks = []
c = 0
while c < cols:
    # check if column c is empty (all spaces)
    if all(matrix[r][c] == " " for r in range(rows)):
        c += 1
        continue
    # start of block
    start = c
    while c < cols and not all(matrix[r][c] == " " for r in range(rows)):
        c += 1
    end = c - 1
    blocks.append((start, end))

total = 0

for start, end in blocks:
    # build strings for each row within this block
    row_strs = []
    for r in range(rows):
        s = "".join(matrix[r][start:end+1]).rstrip()
        row_strs.append(s)

    # find last non-empty row (operator row)
    op_row_idx = None
    for i in range(rows - 1, -1, -1):
        if row_strs[i].strip() != "":
            op_row_idx = i
            break
    if op_row_idx is None:
        continue

    op_row = row_strs[op_row_idx]
    op = "+"
    if "*" in op_row and "+" not in op_row:
        op = "*"
    elif "+" in op_row and "*" not in op_row:
        op = "+"
    else:
        # if both or neither, pick the one that appears rightmost in the operator row
        m = re.search(r'[\+\*](?!.*[\+\*])', op_row)
        if m:
            op = m.group(0)
        else:
            # fallback: look for + anywhere in the block's bottom characters
            if "+" in op_row:
                op = "+"
            else:
                op = "*"

    # extract numbers from rows above the operator row
    nums = []
    for i in range(op_row_idx):
        s = row_strs[i]
        if not s.strip():
            continue
        m = re.search(r'\d+', s)
        if m:
            nums.append(int(m.group(0)))

    if not nums:
        continue

    if op == "+":
        total += sum(nums)
    else:
        prod = 1
        for n in nums:
            prod *= n
        total += prod

print(total)