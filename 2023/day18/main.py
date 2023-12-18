import fileinput

import numpy as np


def shoelace(path):
    xs = np.array([pt[0] for pt in path])
    ys = np.array([pt[1] for pt in path])
    i = np.arange(len(xs))

    area = np.abs(np.sum(xs[i-1]*ys[i]-xs[i]*ys[i-1])*0.5)
    return int(area)


def part1(lines):
    exterior = 0
    path = [(0, 0)]
    for line in lines:
        x, y = path[-1]
        d, n, _ = line.split()
        n = int(n)
        exterior += n
        if d == 'R':
            pt = (x+n, y)
        elif d == 'L':
            pt = (x-n, y)
        elif d == 'U':
            pt = (x, y-n)
        elif d == 'D':
            pt = (x, y+n)
        path.append(pt)
    path = path[:-1]

    area = shoelace(path) + exterior//2 + 1
    return area


def part2(lines):
    exterior = 0
    path = [(0, 0)]
    for line in lines:
        x, y = path[-1]
        _, _, h = line.split()
        n, d = h[2:-2], h[-2]
        d = 'RDLU'[int(d)]
        n = int(n, base=16)
        exterior += n
        if d == 'R':
            pt = (x+n, y)
        elif d == 'L':
            pt = (x-n, y)
        elif d == 'U':
            pt = (x, y-n)
        elif d == 'D':
            pt = (x, y+n)
        path.append(pt)
    path = path[:-1]

    area = shoelace(path) + exterior//2 + 1
    return area


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
