
import sys

# ---------------------------------------
# Input parsing functions
# ---------------------------------------
def parse_input(filename):
    shapes = {}
    regions = []
    
    current_shape_id = None
    current_shape_lines = []
    
    parsing_shapes = True
    
    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip() for line in f]
            
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Detect switching to regions section (lines like "4x4: 0 0...")
            if 'x' in line and ':' in line and not line.endswith(':'):
                parsing_shapes = False
            
            if parsing_shapes:
                if line.endswith(':'):
                    # Save previous shape if exists
                    if current_shape_id is not None and current_shape_lines:
                        shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
                        current_shape_lines = []
                    
                    # Start new shape
                    current_shape_id = int(line[:-1])
                    i += 1
                    continue
                
                if line == '':
                    # Save previous shape if we hit a blank line
                    if current_shape_id is not None and current_shape_lines:
                        shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
                        current_shape_lines = []
                        current_shape_id = None
                else:
                    if current_shape_id is not None:
                        current_shape_lines.append(line)
                        
            else:
                # Parsing Regions
                if line.strip():
                    parts = line.split(':')
                    dims = parts[0].strip().split('x')
                    w, h = int(dims[0]), int(dims[1])
                    
                    counts = [int(x) for x in parts[1].strip().split()]
                    regions.append({
                        'w': w, 'h': h,
                        'counts': counts
                    })
            i += 1
            
        # Capture last shape if file ended abruptly
        if parsing_shapes and current_shape_id is not None and current_shape_lines:
             shapes[current_shape_id] = parse_shape_grid(current_shape_lines)
             
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
        
    return shapes, regions

def parse_shape_grid(lines):
    """Converts list of strings to a set of (r, c) coordinates."""
    coords = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '#':
                coords.add((r, c))
    return normalize_shape(coords)

def normalize_shape(coords):
    """Shifts coords so top-leftmost is at (0,0)."""
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

# ---------------------------------------
# Generate shape variants (rotations + flips)
# ---------------------------------------
def generate_variants(base_shape):
    variants = set()
    
    def rotate(coords):
        return set((c, -r) for r, c in coords)
        
    def flip(coords):
        return set((r, -c) for r, c in coords)

    curr = set(base_shape)
    for _ in range(4):
        variants.add(normalize_shape(curr))
        variants.add(normalize_shape(flip(curr)))
        curr = rotate(curr)
        
    return [list(v) for v in variants]

# ---------------------------------------
# Region solver
# ---------------------------------------
def solve_region(w, h, piece_list, all_variants):
    total_piece_area = 0
    pieces_data = []
    
    for pid in piece_list:
        area = len(all_variants[pid][0])
        total_piece_area += area
        pieces_data.append({'id': pid, 'area': area})
        
    if total_piece_area > w * h:
        return False

    pieces_data.sort(key=lambda x: x['area'], reverse=True)
    sorted_piece_ids = [p['id'] for p in pieces_data]

    grid = [[False for _ in range(w)] for _ in range(h)]

    def can_place(r, c, shape_coords):
        for dr, dc in shape_coords:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                return False
            if grid[nr][nc]:
                return False
        return True

    def place(r, c, shape_coords, val):
        for dr, dc in shape_coords:
            grid[r + dr][c + dc] = val

    def backtrack(idx):
        if idx == len(sorted_piece_ids):
            return True

        pid = sorted_piece_ids[idx]
        variants = all_variants[pid]
        
        for r in range(h):
            for c in range(w):
                if grid[r][c]:
                    continue
                for var in variants:
                    if can_place(r, c, var):
                        place(r, c, var, True)
                        if backtrack(idx + 1):
                            return True
                        place(r, c, var, False)
        return False

    return backtrack(0)

# ---------------------------------------
# Main solve function
# ---------------------------------------
def solve():
    print("Parsing input from input.txt...")
    shapes, regions = parse_input('E:\Advent of Code\AOC 25\Day-12\input.txt')
    
    all_variants = {sid: generate_variants(coords) for sid, coords in shapes.items()}
        
    solvable_count = 0
    
    print(f"Processing {len(regions)} regions...")
    
    for i, reg in enumerate(regions):
        piece_list = []
        for sid, count in enumerate(reg['counts']):
            piece_list.extend([sid] * count)
            
        print(f"Region {i}: {reg['w']}x{reg['h']}, {len(piece_list)} pieces... ", end="")
        sys.stdout.flush()
        
        if solve_region(reg['w'], reg['h'], piece_list, all_variants):
            print("Fits!")
            solvable_count += 1
        else:
            print("No fit.")
            
    print("-" * 30)
    print(f"Total solvable regions: {solvable_count}")

# ---------------------------------------
# Entry point
# ---------------------------------------
if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    solve()