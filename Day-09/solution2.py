
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
        layout.extend([str(file_id)] * length)
        file_id += 1
    else:
        layout.extend(["."] * length)

files_info = {}
curr_id = None
count = 0
for i, ch in enumerate(layout):
    if ch != ".":
        fid = int(ch)
        if fid != curr_id:
            curr_id = fid
            count = 1
            files_info[fid] = [i, 1]
        else:
            count += 1
            files_info[fid][1] = count

max_file_id = max(files_info.keys())


def find_free_span(layout, file_start, file_length):
    if file_start == 0:
        return None
    best_span_start = None
    curr_start = None
    curr_count = 0
    for i in range(file_start):
        if layout[i] == ".":
            if curr_start is None:
                curr_start = i
                curr_count = 1
            else:
                curr_count += 1
        else:
            if curr_count >= file_length:
                return curr_start
            curr_start = None
            curr_count = 0
    if curr_start is not None and curr_count >= file_length:
        return curr_start
    return None


for fid in sorted(files_info.keys(), reverse=True):
    start_pos, length = files_info[fid]
    span_start = find_free_span(layout, start_pos, length)
    if span_start is not None:
        for i in range(start_pos, start_pos + length):
            layout[i] = "."
        for i in range(span_start, span_start + length):
            layout[i] = str(fid)
        files_info[fid][0] = span_start

checksum = 0
for i, ch in enumerate(layout):
    if ch != ".":
        checksum += i * int(ch)

print(checksum)