import fileinput
import itertools

from shapely.geometry import Point, Polygon

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?

def parse(lines):
    pts = []
    for line in lines:
        x, y = line.split(',')
        x, y = int(x), int(y)
        pts.append((x, y))
    return pts

def area(a, b):
    w = abs(a[0]-b[0]) + 1
    h = abs(a[1]-b[1]) + 1
    return w * h


def part1(lines):
    pts = parse(lines)

    best = 0
    for a, b in itertools.combinations(pts, 2):
        ar = area(a, b)
        if ar > best:
            best = ar
    return best


def part2(lines):
    pts = parse(lines)
    poly = Polygon(pts)

    best = 0
    for a, b in itertools.combinations(pts, 2):
        ax, ay = a
        bx, by = b

        rect = Polygon([
            a,             # TL
            (a[0], b[1]),  # BL
            b,             # BR
            (b[0], a[1]),  # TR
        ])
        if not poly.contains(rect):
            continue

        ar = area(a, b)
        if ar > best:
            best = ar

    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
