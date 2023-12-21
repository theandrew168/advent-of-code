import fileinput


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.w = len(lines[0])
        self.h = len(lines)

    def get(self, pt):
        x, y = pt
        return self.lines[y][x]

    def adj(self, pt):
        x, y = pt
        for yoff in [-1, 1]:
            yy = y + yoff
            if yy < 0 or yy >= self.h:
                continue
            yield x, yy
        for xoff in [-1, 1]:
            xx = x + xoff
            if xx < 0 or xx >= self.w:
                continue
            yield xx, y


def find_start(grid):
    for y in range(grid.h):
        for x in range(grid.w):
            pt = (x, y)
            if grid.get(pt) == 'S':
                return pt
    assert False


def part1(lines):
    grid = Grid(lines)
    start = find_start(grid)

    curr = set()
    curr.add(start)
    for _ in range(64):
        nxt = set()
        for pt in curr:
            for adj in grid.adj(pt):
                c = grid.get(adj)
                if c == '#':
                    continue
                nxt.add(adj)
        curr = nxt

    return len(curr)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
