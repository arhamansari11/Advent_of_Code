from __future__ import annotations
import z3  # or import z4 as z3 if you're using z4
import random
from functools import cache
from itertools import product, combinations
from collections import defaultdict, deque

# Utility functions that were in util.py
def lines(s: str):
    return s.strip().split('\n')

def bfs(adj, start):
    dist = {start: 0}
    prev = {start: None}
    q = deque([start])
    
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = u
                q.append(v)
    
    return dist, prev

def topsort(adj):
    indeg = defaultdict(int)
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    
    q = deque()
    for u in adj:
        if indeg[u] == 0:
            q.append(u)
    
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    
    return order, len(order) != len(adj)

# Read from input.txt
with open("input.txt", "r") as f:
    A, B = f.read().split("\n\n")

G = dict()
for l in lines(A):
    a, b = l.split(": ")
    G[a] = int(b)

ops = {}
for l in lines(B):
    x, dest = l.split(" -> ")
    a, op, b = x.split()
    ops[dest] = (a, op, b)

zs = {s for s in ops if s[0] == "z"}
zs = sorted(zs, key=lambda x: int(x[1:]), reverse=True)

def sim(G):
    n = len(zs)
    i = 0
    while i < n:
        for d, (a, op, b) in ops.items():
            if d in G:
                continue
            if a in G and b in G:
                x, y = G[a], G[b]
                if op == "AND":
                    G[d] = x & y
                elif op == "OR":
                    G[d] = x | y
                elif op == "XOR":
                    G[d] = x ^ y
                else:
                    assert False

                if d in zs:
                    i += 1

    return int("".join(str(G[z]) for z in zs), 2)

def mkadj():
    adj = {s: [a, b] for s, (a, _, b) in ops.items()}
    for s in G:
        adj[s] = []
    return adj

def is_cyclic():
    return topsort(mkadj())[1]

def swappable(s: str):
    return set(bfs(mkadj(), s)[1]) - set(G)

@cache
def testf(i: int):
    DIFF = 6
    if i < DIFF:
        tests = list(product(range(1 << i), repeat=2))
    else:
        tests = []
        for _ in range(1 << (2*DIFF)):
            a = random.randrange(1 << i)
            b = random.randrange(1 << i)
            tests.append((a, b))

    random.shuffle(tests)
    return tests

def f(i: int, swapped: set[str]):
    if i == 46:
        res = ",".join(sorted(swapped))
        print(f"Answer: {res}")
        return

    def getv(s: str, a: int, b: int) -> int:
        if s[0] == "x":
            return (a >> int(s[1:])) & 1
        if s[0] == "y":
            return (b >> int(s[1:])) & 1
        av, op, bv = ops[s]
        x, y = getv(av, a, b), getv(bv, a, b)
        if op == "AND":
            return x & y
        if op == "OR":
            return x | y
        if op == "XOR":
            return x ^ y

    def check():
        for a, b in testf(i):
            for j in range(i+1):
                x = getv(f"z{j:02}", a, b)
                if x != ((a + b) >> j) & 1:
                    return False
        return True

    works = check()
    print(i, works, swapped)
    if works:
        f(i+1, swapped)
        return

    if len(swapped) == 8:
        return

    inside = swappable(f"z{i:02}") - swapped
    outside = set(ops) - swapped
    to_test = list(product(inside, outside)) + list(combinations(inside, 2))
    random.shuffle(to_test)

    for a, b in to_test:
        if a == b: continue
        ops[a], ops[b] = ops[b], ops[a]
        swapped.add(a)
        swapped.add(b)
        if not is_cyclic() and check():
            f(i, swapped)
        swapped.remove(a)
        swapped.remove(b)
        ops[a], ops[b] = ops[b], ops[a]

# Start the search
f(0, set())