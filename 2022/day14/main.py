from collections import namedtuple
import fileinput

from more_itertools import windowed


class Overflow(Exception):
    pass


Point = namedtuple('Point', 'x y')


class Grid:

    def __init__(self, lines, floor=False, pour=Point(500, 0)):
        self.pour = pour

        self.grid = {pour: '+'}
        for line in lines:
            segs = line.split(' -> ')
            for a, b in windowed(segs, 2):
                ax, ay = a.split(',')
                ax, ay = int(ax), int(ay)
                bx, by = b.split(',')
                bx, by = int(bx), int(by)
                # vertical
                if ax == bx:
                    start, end = min([ay, by]), max([ay, by])
                    for y in range(start, end + 1):
                        p = Point(ax, y)
                        self.grid[p] = '#'
                # horizontal
                else:
                    start, end = min([ax, bx]), max([ax, bx])
                    for x in range(start, end + 1):
                        p = Point(x, ay)
                        self.grid[p] = '#'

        if floor:
            lvl = max(p.y for p in self.grid) + 2
            for x in range(-1000, 1000):
                p = Point(self.pour.x + x, lvl)
                self.grid[p] = '#'

        self.lbx, self.ubx = min(p.x for p in self.grid), max(p.x for p in self.grid)
        self.lby, self.uby = min(p.y for p in self.grid), max(p.y for p in self.grid)

    def __str__(self):
        width, height = self.ubx - self.lbx + 1, self.uby - self.lby + 1

        s = ''
        for y in range(height):
            for x in range(width):
                p = Point(self.lbx + x, self.lby + y)
                s += self.grid.get(p, '.')
            s += '\n'

        return s

    def sim(self, edge=True):
        tops = [
            Point(self.pour.x, self.pour.y + 1),
            Point(self.pour.x - 1, self.pour.y + 1),
            Point(self.pour.x + 1, self.pour.y + 1),
        ]

        s = self.pour
        while True:
            # reached top
            if all(p in self.grid for p in tops):
                raise Overflow()

            # fell off edge
            if edge and not [p for p in self.grid if p.x == s.x]:
                raise Overflow()

            down = Point(s.x, s.y + 1)
            down_left = Point(down.x - 1, down.y)
            down_right = Point(down.x + 1, down.y)

            if down not in self.grid:
                s = down
                continue

            if down_left not in self.grid:
                s = down_left
                continue

            if down_right not in self.grid:
                s = down_right
                continue

            break
        
        self.grid[s] = 'o'


def part1(lines):
    score = 0

    grid = Grid(lines)
    while True:
        try:
            grid.sim()
        except Overflow:
            break
        else:
            score += 1

    return score


def part2(lines):
    score = 0

    grid = Grid(lines, floor=True)
    while True:
        try:
            grid.sim(edge=False)
        except Overflow:
            break
        else:
            score += 1

    return score + 1


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
