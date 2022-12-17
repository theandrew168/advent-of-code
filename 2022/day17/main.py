from collections import defaultdict, namedtuple
import fileinput
from itertools import cycle


WIDTH = 7

Point = namedtuple('Point', 'x y')


def p1(o):
    """
    ####
    """
    ps = [
        Point(o.x, o.y),
        Point(o.x + 1, o.y),
        Point(o.x + 2, o.y),
        Point(o.x + 3, o.y),
    ]
    return set(ps)


def p2(o):
    """
    .#.
    ###
    .#.
    """
    ps = [
        Point(o.x + 1, o.y),
        Point(o.x, o.y + 1),
        Point(o.x + 1, o.y + 1),
        Point(o.x + 2, o.y + 1),
        Point(o.x + 1, o.y + 2),
    ]
    return set(ps)


def p3(o):
    """
    ..#
    ..#
    ###
    """
    ps = [
        Point(o.x, o.y),
        Point(o.x + 1, o.y),
        Point(o.x + 2, o.y),
        Point(o.x + 2, o.y + 1),
        Point(o.x + 2, o.y + 2),
    ]
    return set(ps)


def p4(o):
    """
    #
    #
    #
    #
    """
    ps = [
        Point(o.x, o.y),
        Point(o.x, o.y + 1),
        Point(o.x, o.y + 2),
        Point(o.x, o.y + 3),
    ]
    return set(ps)


def p5(o):
    """
    ##
    ##
    """
    ps = [
        Point(o.x, o.y),
        Point(o.x + 1, o.y),
        Point(o.x, o.y + 1),
        Point(o.x + 1, o.y + 1),
    ]
    return set(ps)


def left(board, points):
    if min(p.x for p in points) <= 0:
        return points, False

    moved = set(Point(p.x - 1, p.y) for p in points)
    if board & moved:
        return points, False

    return moved, True


def right(board, points):
    if max(p.x for p in points) >= WIDTH - 1:
        return points, False

    moved = set(Point(p.x + 1, p.y) for p in points)
    if board & moved:
        return points, False

    return moved, True


def down(board, points):
    if min(p.y for p in points) <= 0:
        return points, False

    moved = set(Point(p.x, p.y - 1) for p in points)
    if board & moved:
        return points, False

    return moved, True


def display(lines, start, count):
    end = start + count

    s = []
    for y in sorted(lines.keys())[start:end]:

        l = ''
        for x in range(WIDTH):
            if x in lines[y]:
                l += '#'
            else:
                l += '.'
        s.append(l)

    return '\n'.join(reversed(s))


def part1(line):
    board = set()
    origin = Point(2, 3)
    pieces = cycle([p1, p2, p3, p4, p5])
    highest = 0
    rocks = 0

    piece = next(pieces)
    active = piece(origin)
    for c in cycle(line):
        if c == '<':
            active, _ = left(board, active)
        else:
            active, _ = right(board, active)

        active, moved = down(board, active)
        if not moved:
            top = max(p.y for p in active)
            if top > highest:
                highest = top

            board |= active
            origin = Point(2, highest + 4)
            piece = next(pieces)
            active = piece(origin)
            rocks += 1

        if rocks >= 2022:
            return highest + 1


# 1566984124796 high
# 1566272189352
# 1566272188766 low
def part2(line):
    board = set()
    origin = Point(2, 3)
    pieces = cycle([p1, p2, p3, p4, p5])
    highest = 0
    rocks = 0

    lines = defaultdict(set)
    heights = {}

    piece = next(pieces)
    active = piece(origin)

    for c in cycle(line):
        if c == '<':
            active, _ = left(board, active)
        else:
            active, _ = right(board, active)

        active, moved = down(board, active)
        if not moved:
            top = max(p.y for p in active)
            if top > highest:
                highest = top
                heights[highest] = rocks

            for p in active:
                lines[p.y].add(p.x)

            board |= active
            origin = Point(2, highest + 4)
            piece = next(pieces)
            active = piece(origin)
            rocks += 1

            # simulate the first few rocks
            if rocks >= 5000:
                break

    chunk = 25
    start_height = None
    end_height = None
    for i in range(1000):
        pattern = display(lines, i, chunk)
        for j in range(i + 1, highest):
            check = display(lines, j, chunk)
            if check == pattern:
                print('pattern:', i)
                print(pattern)
                print('found at height:', j)
                start_height = i
                end_height = j
                break

        if start_height:
            break

    cycle_height = end_height - start_height
    start_rocks = heights[min(k for k in heights if k >= start_height)]
    rps = heights[min(k for k in heights if k >= end_height)] - heights[min(k for k in heights if k >= start_height)]
    cs = (1000000000000 - start_rocks) // rps
    return start_height + (cs * cycle_height) 


if __name__ == '__main__':
    line = None
    for line in fileinput.input():
        line = line.strip()

    print(part1(line))
    print(part2(line))
