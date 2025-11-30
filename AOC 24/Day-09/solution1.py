from pathlib import Path

# fn = "ex1.txt"
fn = "e:/Advent of Code/Day-09/input.txt"
#fn = Path(Path(__file__).parent, fn)
dat = open(fn).read().strip().split("\n")

s = dat[0]
files = []
layout = []
file_id = 0
for i, ch in enumerate(s):
    length = int(ch)
    if i % 2 == 0:
        # file blocks
        layout.extend([str(file_id)] * length)
        file_id += 1
    else:
        layout.extend(["."] * length)

while True:
    try:
        gap_index = layout.index(".")
    except ValueError:
        break

    found_file_to_the_right = any(ch != "." for ch in layout[gap_index + 1 :])
    if not found_file_to_the_right:
        break

    for i in range(len(layout) - 1, -1, -1):
        if layout[i] != ".":
            layout[gap_index], layout[i] = layout[i], "."
            break

checksum = 0
for i, ch in enumerate(layout):
    if ch != ".":
        checksum += i * int(ch)

print(checksum)