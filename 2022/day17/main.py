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


def display(board):
    lines = defaultdict(set)
    for p in board:
        lines[p.y].add(p.x)

    print(lines)
    for y in reversed(sorted(lines.keys())):
        s = ''
        for x in range(WIDTH):
            if x in lines[y]:
                s += '#'
            else:
                s += '.'
        print(s)


def solve(line, limit):
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

        if rocks >= limit:
            return highest + 1


if __name__ == '__main__':
    line = None
    for line in fileinput.input():
        line = line.strip()

    print(solve(line, 2022))
    #print(solve(line, 1000000000))
