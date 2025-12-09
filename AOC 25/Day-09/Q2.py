from bisect import bisect_left, bisect_right
#https://docs.python.org/3/library/bisect.html

def parse_input(input_text):
    lines = input_text.strip().split('\n')
    
    red_tiles = []
    for line in lines:
        if line.strip():
            x, y = line.strip().split(',')
            red_tiles.append((int(x), int(y)))
    
    return red_tiles


def build_boundary_segments(red_tiles):
    horizontal_segments = {}
    vertical_segments = []
    boundary_ys = set()
    
    for i in range(len(red_tiles)):
        tile1 = red_tiles[i]
        tile2 = red_tiles[(i + 1) % len(red_tiles)]
        x1, y1 = tile1
        x2, y2 = tile2
        
        if y1 == y2:
            min_x, max_x = min(x1, x2), max(x1, x2)
            if y1 not in horizontal_segments:
                horizontal_segments[y1] = []
            horizontal_segments[y1].append((min_x, max_x))
            boundary_ys.add(y1)
        elif x1 == x2:
            min_y, max_y = min(y1, y2), max(y1, y2)
            vertical_segments.append((x1, min_y, max_y))
            boundary_ys.add(min_y)
            boundary_ys.add(max_y)
    
    vertical_segments.sort(key=lambda s: s[1])
    
    return horizontal_segments, vertical_segments, sorted(boundary_ys)


def compute_x_bounds_by_y(horizontal_segments, vertical_segments, all_ys):
    x_bounds_by_y = {}
    
    for y in all_ys:
        x_ranges = []
        
        if y in horizontal_segments:
            x_ranges.extend(horizontal_segments[y])
        
        for seg_x, seg_min_y, seg_max_y in vertical_segments:
            if seg_min_y <= y <= seg_max_y:
                x_ranges.append((seg_x, seg_x))
        
        if not x_ranges:
            continue
        
        x_ranges.sort()
        
        merged = []
        for start, end in x_ranges:
            if merged and start <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        
        x_bounds_by_y[y] = (merged[0][0], merged[-1][1])
    
    return x_bounds_by_y


def is_valid_rectangle(min_x, max_x, min_y, max_y, x_bounds_by_y, boundary_ys):
    left = bisect_left(boundary_ys, min_y)
    right = bisect_right(boundary_ys, max_y)
    
    ys_to_check = [min_y, max_y]
    for i in range(left, right):
        y = boundary_ys[i]
        ys_to_check.append(y)
        if y > min_y:
            ys_to_check.append(y - 1)
        if y < max_y:
            ys_to_check.append(y + 1)
    
    for y in ys_to_check:
        if y < min_y or y > max_y:
            continue
        
        if y not in x_bounds_by_y:
            return False
        
        bound_min_x, bound_max_x = x_bounds_by_y[y]
        
        if min_x < bound_min_x or max_x > bound_max_x:
            return False
    
    return True


def find_largest_rectangle(red_tiles, x_bounds_by_y, boundary_ys):
    n = len(red_tiles)
    
    candidate_pairs = []
    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            if width > 0 and height > 0:
                area = (width + 1) * (height + 1)
                candidate_pairs.append((area, i, j))
    
    candidate_pairs.sort(reverse=True)
    
    for area, i, j in candidate_pairs:
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        min_x, max_x = (x1, x2) if x1 < x2 else (x2, x1)
        min_y, max_y = (y1, y2) if y1 < y2 else (y2, y1)
        
        if is_valid_rectangle(min_x, max_x, min_y, max_y, x_bounds_by_y, boundary_ys):
            return area, (red_tiles[i], red_tiles[j])
    
    return 0, None


def solve(input_text):
    red_tiles = parse_input(input_text)
    
    horizontal_segments, vertical_segments, boundary_ys = build_boundary_segments(red_tiles)
    
    all_ys = set(boundary_ys)
    for y in boundary_ys:
        all_ys.add(y - 1)
        all_ys.add(y + 1)
    for tile in red_tiles:
        all_ys.add(tile[1])
    
    x_bounds_by_y = compute_x_bounds_by_y(horizontal_segments, vertical_segments, all_ys)
    
    max_area, best_pair = find_largest_rectangle(red_tiles, x_bounds_by_y, boundary_ys)
    
    print(f"\nNumber of red tiles: {len(red_tiles)}")
    print(f"Best pair: {best_pair}")
    print(f"Largest rectangle area: {max_area}")
    return max_area


if __name__ == "__main__":
    with open("E:\Advent of Code\AOC 25\Day-09\input.txt", "r") as f:
        input_text = f.read()
    
    solve(input_text)