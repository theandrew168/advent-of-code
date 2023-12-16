import fileinput

import sys
sys.setrecursionlimit(100000)


class Grid:

    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def get(self, x, y):
        return self.lines[y][x]


def trace(grid, seen, curr):
    if curr in seen:
        return

    x, y, d = curr
    if x < 0 or x >= grid.width:
        return
    if y < 0 or y >= grid.height:
        return

    seen.add(curr)

    c = grid.get(x, y)
    if c == '.':
        if d == 'N':
            trace(grid, seen, (x, y-1, d))
        elif d == 'S':
            trace(grid, seen, (x, y+1, d))
        elif d == 'E':
            trace(grid, seen, (x+1, y, d))
        elif d == 'W':
            trace(grid, seen, (x-1, y, d))
    elif c == '|':
        if d == 'N':
            trace(grid, seen, (x, y-1, d))
        elif d == 'S':
            trace(grid, seen, (x, y+1, d))
        else:
            trace(grid, seen, (x, y-1, 'N'))
            trace(grid, seen, (x, y+1, 'S'))
    elif c == '-':
        if d == 'E':
            trace(grid, seen, (x+1, y, d))
        elif d == 'W':
            trace(grid, seen, (x-1, y, d))
        else:
            trace(grid, seen, (x+1, y, 'E'))
            trace(grid, seen, (x-1, y, 'W'))
    elif c == '/':
        if d == 'N':
            trace(grid, seen, (x+1, y, 'E'))
        elif d == 'S':
            trace(grid, seen, (x-1, y, 'W'))
        elif d == 'E':
            trace(grid, seen, (x, y-1, 'N'))
        elif d == 'W':
            trace(grid, seen, (x, y+1, 'S'))
    elif c == '\\':
        if d == 'N':
            trace(grid, seen, (x-1, y, 'W'))
        elif d == 'S':
            trace(grid, seen, (x+1, y, 'E'))
        elif d == 'E':
            trace(grid, seen, (x, y+1, 'S'))
        elif d == 'W':
            trace(grid, seen, (x, y-1, 'N'))


def part1(lines):
    grid = Grid(lines)

    curr = (0, 0, 'E')
    seen = set()
    trace(grid, seen, curr)
    uniq = set(p[:-1] for p in seen)
    return len(uniq)


def part2(lines):
    grid = Grid(lines)
    best = None

    for x in range(grid.width):
        curr = (x, 0, 'S')
        seen = set()
        trace(grid, seen, curr)
        uniq = set(p[:-1] for p in seen)
        if best is None or len(uniq) > best:
            best = len(uniq)

        curr = (x, grid.height-1, 'N')
        seen = set()
        trace(grid, seen, curr)
        uniq = set(p[:-1] for p in seen)
        if best is None or len(uniq) > best:
            best = len(uniq)

    for y in range(grid.height):
        curr = (0, y, 'E')
        seen = set()
        trace(grid, seen, curr)
        uniq = set(p[:-1] for p in seen)
        if best is None or len(uniq) > best:
            best = len(uniq)

        curr = (grid.width-1, y, 'W')
        seen = set()
        trace(grid, seen, curr)
        uniq = set(p[:-1] for p in seen)
        if best is None or len(uniq) > best:
            best = len(uniq)

    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
