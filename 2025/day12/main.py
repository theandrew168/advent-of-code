from collections import Counter, defaultdict, deque
import fileinput
import functools
import itertools
from pprint import pprint
from queue import PriorityQueue

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def parse(lines):
    shapes = []
    regions = []

    curr_shape = None
    for line in lines:
        if not line:
            continue

        if 'x' in line:
            wh, vals = line.split(': ')
            w, h = wh.split('x')
            w, h = int(w), int(h)
            vals = [int(v) for v in vals.split()]
            regions.append((w, h, vals))
            continue

        if ':' in line:
            if curr_shape:
                shapes.append(curr_shape)
            curr_shape = []
        else:
            curr_shape.append(list(line))

    shapes.append(curr_shape)
    return shapes, regions


def part1(lines):
    shapes, regions = parse(lines)

    sizes = []
    for shape in shapes:
        size = 0
        for row in shape:
            for c in row:
                if c == '#':
                    size += 1
        sizes.append(size)

    total = 0
    for w, h, vals in regions:
        area = w * h

        impossible = False
        trivial = False

        # check if impossible because not enough space
        score = 0
        for i, val in enumerate(vals):
            score += val * sizes[i]
        if score > area:
            impossible = True

        # check if trivial because all pieces fit without fitting
        score = 0
        for i, val in enumerate(vals):
            shape = shapes[i]
            sw, sh = len(shape[0]), len(shape)
            score += val * sw * sh
        if score <= area:
            trivial = True

        if impossible:
            continue
        elif trivial:
            total += 1
        else:
            print('needs further analysis')

    return total


def part2(lines):
    return 'See you next year! Happy Holidays!'


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
