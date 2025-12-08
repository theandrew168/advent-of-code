import fileinput
import itertools
import math
from pprint import pprint

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def parse(line):
    x, y, z = line.split(',')
    x, y, z = int(x), int(y), int(z)
    return (x, y, z)


def dist(a, b):
    x2 = (b[0] - a[0]) ** 2
    y2 = (b[1] - a[1]) ** 2
    z2 = (b[2] - a[2]) ** 2
    return math.sqrt(x2 + y2 + z2)


def part1(lines):
    pts = [parse(line) for line in lines]

    bykey = {}
    bydist = {}
    for a, b in itertools.combinations(pts, 2):
        key = frozenset([a, b])
        if key in bykey:
            continue
        d = dist(a, b)
        bykey[key] = d
        bydist[d] = (a, b)

    cs = set()
    ds = sorted(bydist.keys())

    N = 10 if len(lines) == 20 else 1000
    for d in ds[:N]:
        a, b = bydist[d]

        ac = [c for c in cs if a in c]
        ac = ac[0] if ac else None

        bc = [c for c in cs if b in c]
        bc = bc[0] if bc else None

        if ac and bc:
            # same: skip
            if ac == bc:
                continue
            # merge
            nc = frozenset(ac | bc)
            cs.remove(ac)
            cs.remove(bc)
            cs.add(nc)
        elif ac:
            # add to ac
            nc = set(ac)
            nc.add(b)
            nc = frozenset(nc)
            cs.remove(ac)
            cs.add(nc)
        elif bc:
            # add to bc
            nc = set(bc)
            nc.add(a)
            nc = frozenset(nc)
            cs.remove(bc)
            cs.add(nc)
        else:
            # new circuit
            nc = frozenset([a, b])
            cs.add(nc)

    ls = sorted([len(c) for c in cs], reverse=True)
    return math.prod(ls[:3])


def part2(lines):
    pts = [parse(line) for line in lines]

    bykey = {}
    bydist = {}
    for a, b in itertools.combinations(pts, 2):
        key = frozenset([a, b])
        if key in bykey:
            continue
        d = dist(a, b)
        bykey[key] = d
        bydist[d] = (a, b)

    cs = set()
    ds = sorted(bydist.keys())

    for d in ds:
        a, b = bydist[d]

        ac = [c for c in cs if a in c]
        ac = ac[0] if ac else None

        bc = [c for c in cs if b in c]
        bc = bc[0] if bc else None

        if ac and bc:
            # same: skip
            if ac == bc:
                continue
            # merge
            nc = frozenset(ac | bc)
            cs.remove(ac)
            cs.remove(bc)
            cs.add(nc)
        elif ac:
            # add to ac
            nc = set(ac)
            nc.add(b)
            nc = frozenset(nc)
            cs.remove(ac)
            cs.add(nc)
        elif bc:
            # add to bc
            nc = set(bc)
            nc.add(a)
            nc = frozenset(nc)
            cs.remove(bc)
            cs.add(nc)
        else:
            # new circuit
            nc = frozenset([a, b])
            cs.add(nc)

        # one circuit with all boxes
        if len(cs) == 1 and len(list(cs)[0]) == len(lines):
            return a[0] * b[0]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
