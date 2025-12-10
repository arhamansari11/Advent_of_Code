


#!/usr/bin/env python3
"""
Solve the Factory (lights & buttons) problem.
Reads input from a file named `input.txt` in the current working directory and
prints the fewest total button presses required to configure ALL machines.

Each line in input.txt must follow the format shown in the problem statement,
for example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

The code ignores the numbers in {curly braces}.

Approach:
- For each machine we form a linear system over GF(2): A x = b, where columns of
  A are buttons and rows are lights. b is the target pattern (# -> 1, . -> 0).
- Use Gaussian elimination to find a particular solution and a basis for the
  nullspace. Because pressing a button twice cancels out, each button is either
  pressed 0 or 1 times (mod 2). Among all solutions we choose one with minimum
  Hamming weight (minimum number of button presses).
- If the nullspace dimension is small (<=24) we brute-force all combinations of
  nullspace basis vectors to find the minimum weight solution.
- If the nullity is larger, a greedy local search tries to reduce weight (this
  is unlikely to be necessary on typical inputs but is a safe fallback).

Output:
Prints a single integer: the minimal total presses summed over all machines.

"""

from typing import List, Tuple
import re
import sys


def parse_line(line: str) -> Tuple[List[int], int, int]:
    """Parse a single line and return (button_masks, num_lights, target_mask).

    button_masks: list of integers where bit j (1<<j) corresponds to button j
                  being pressed toggles the (j-th?) WAIT: we store masks with
                  bits corresponding to buttons, but elimination is done row-wise
                  so we'll convert as needed.
    num_lights: number of indicator lights
    target_mask: integer mask of lights target state (bit i = 1 if light i should be ON)
    """
    line = line.strip()
    if not line:
        return [], 0, 0

    # Extract bracket pattern
    m = re.search(r"\[([^\]]+)\]", line)
    if not m:
        raise ValueError("Couldn't find bracketed lights pattern")
    pattern = m.group(1).strip()
    n = len(pattern)
    target_mask = 0
    for i, ch in enumerate(pattern):
        if ch == '#':
            target_mask |= (1 << i)

    # Extract parentheses groups (buttons). They appear after the bracket.
    buttons = re.findall(r"\(([^)]*)\)", line)
    button_masks = []
    for b in buttons:
        b = b.strip()
        if b == '':
            # empty button does nothing
            button_masks.append(0)
            continue
        # numbers separated by commas
        idxs = [int(x) for x in re.split(r"\s*,\s*", b) if x != '']
        mask = 0
        for idx in idxs:
            if idx < 0 or idx >= n:
                # ignore out-of-range indices (defensive)
                continue
            # set bit for this light in the button mask
            mask |= (1 << idx)
        button_masks.append(mask)

    # Ignore curly braces
    return button_masks, n, target_mask


def gauss_elim_gf2(rows: List[int], rhs: int, m: int) -> Tuple[bool, List[int], List[int]]:
    """
    Perform Gaussian elimination on a system with `m` variables (buttons) and
    len(rows) equations (lights). `rows` is a list of integers where bit j
    corresponds to coefficient of variable j in that equation. rhs is integer
    representing right-hand side bits of each equation stacked into bits.

    Returns (is_solvable, solution_particular, nullspace_basis)
    - If not solvable returns (False, [], [])
    - solution_particular is any particular solution (length m list of 0/1 ints)
    - nullspace_basis is a list of basis vectors (each is int mask over m vars)

    Implementation detail: we operate on a copy of rows and rhs and keep track
    of pivot columns.
    """
    R = rows[:]  # copy
    b = rhs
    n = len(R)
    # pivot_col_for_row: which variable is pivot for a given row index, -1 if none
    pivot_col_for_row = [-1] * n
    pivot_row_for_col = [-1] * m

    row = 0
    for col in range(m):
        # find a row >= row with a 1 in this col
        sel = -1
        for r in range(row, n):
            if (R[r] >> col) & 1:
                sel = r
                break
        if sel == -1:
            continue
        # swap rows sel and row
        if sel != row:
            R[sel], R[row] = R[row], R[sel]
            # swap corresponding rhs bits
            bit_sel = (b >> sel) & 1
            bit_row = (b >> row) & 1
            if bit_sel != bit_row:
                # flip bits sel and row in b
                b ^= (1 << sel) | (1 << row)
        pivot_col_for_row[row] = col
        pivot_row_for_col[col] = row

        # eliminate col from other rows
        for r in range(n):
            if r != row and ((R[r] >> col) & 1):
                R[r] ^= R[row]
                # flip rhs bit r if needed
                if ((b >> row) & 1):
                    # b_r ^= b_row
                    b ^= (1 << r)
        row += 1
        if row == n:
            break

    # After elimination check for inconsistency: any zero row with rhs 1
    for r in range(n):
        if R[r] == 0 and ((b >> r) & 1):
            return False, [], []

    # Construct particular solution: set all free vars to 0
    sol = 0
    for col in range(m):
        prow = pivot_row_for_col[col]
        if prow != -1:
            # variable col = rhs of pivot row after elimination
            if (b >> prow) & 1:
                sol |= (1 << col)
        else:
            # free var, leave as 0
            pass

    # Build nullspace basis: for each free variable f, set f=1 and dependent vars accordingly
    basis = []
    for col in range(m):
        if pivot_row_for_col[col] == -1:
            vec = 1 << col
            # for each pivot variable, determine its value when free var is 1
            for c in range(m):
                prow = pivot_row_for_col[c]
                if prow != -1:
                    # if pivot row has coefficient 1 for free var col, then pivot var flips
                    if (R[prow] >> col) & 1:
                        vec |= (1 << c)
            basis.append(vec)

    # return sol as int bitmask and basis as list of int masks
    return True, sol, basis


def min_weight_solution(sol0: int, basis: List[int], m: int) -> int:
    """Find minimum popcount of sol0 xor linear combination of basis vectors.

    If nullity small (<=24) brute force all combinations. Otherwise use greedy
    local improvement as fallback.
    Returns minimal weight (number of 1 bits) for solution over m variables.
    """
    k = len(basis)
    if k == 0:
        return sol0.bit_count()

    if k <= 24:
        best = m + 1
        # iterate over all 2^k combinations
        for mask in range(1 << k):
            v = sol0
            mm = mask
            i = 0
            while mm:
                if mm & 1:
                    v ^= basis[i]
                mm >>= 1
                i += 1
            w = v.bit_count()
            if w < best:
                best = w
        return best
    else:
        # Greedy local search: start from sol0 and try flipping basis vectors if it lowers weight
        v = sol0
        improved = True
        best = v.bit_count()
        # try several passes
        for _ in range(5):
            improved = False
            for b in basis:
                newv = v ^ b
                nw = newv.bit_count()
                if nw < best:
                    v = newv
                    best = nw
                    improved = True
            if not improved:
                break
        return best


def solve_file(filename: str) -> int:
    total = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                button_masks, n, target = parse_line(line)
            except Exception as e:
                print(f"Error parsing line {lineno}: {e}", file=sys.stderr)
                continue
            m = len(button_masks)
            # Build system: rows for each light (n rows), columns for each button (m cols)
            rows = []
            for i in range(n):
                rowmask = 0
                for j, bmask in enumerate(button_masks):
                    if (bmask >> i) & 1:
                        rowmask |= (1 << j)
                rows.append(rowmask)
            rhs = target  # bit i of rhs corresponds to light i

            if m == 0:
                # no buttons: check if target is all zeros
                if target != 0:
                    print(f"Line {lineno}: impossible to achieve target (no buttons)", file=sys.stderr)
                    # treat as unsolvable -> add 0 or raise? we'll add 0
                continue

            ok, sol0, basis = gauss_elim_gf2(rows, rhs, m)
            if not ok:
                print(f"Line {lineno}: no solution", file=sys.stderr)
                continue
            best = min_weight_solution(sol0, basis, m)
            total += best
    return total


if __name__ == '__main__':
    fname = "E:\Advent of Code\AOC 25\Day-10\input.txt"
    total = solve_file(fname)
    print(total)
