import fileinput


class Grid:

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def get(self, x, y):
        idx = y * self.width + x
        return self.data[idx]

    def adjacent(self, x, y):
        adj = []

        for offset in [-1, 1]:
            xx = x + offset
            if xx < 0 or xx >= self.width:
                continue
            adj.append(self.get(xx, y))

        for offset in [-1, 1]:
            yy = y + offset
            if yy < 0 or yy >= self.height:
                continue
            adj.append(self.get(x, yy))

        return adj


def part1(grid):
    lows = []
    for y in range(grid.height):
        for x in range(grid.width):
            p = grid.get(x, y)
            adj = grid.adjacent(x, y)
            if all(p < pp for pp in adj):
                lows.append(p)

    return sum(p + 1 for p in lows)


def part2(grid):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    width = len(lines[0])
    height = len(lines)
    data = [int(n) for n in ''.join(lines)]

    grid = Grid(data, width, height)

    print(part1(grid))
    print(part2(grid))
