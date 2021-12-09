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

    def fill(self, x, y, seen=None):
        if seen is None:
            seen = set()

        p = self.get(x, y)
        if p == 9:
            return seen

        seen.add((x, y))

        for offset in [-1, 1]:
            xx = x + offset
            if xx < 0 or xx >= self.width:
                continue
            if (xx, y) in seen:
                continue
            seen.update(self.fill(xx, y, seen))

        for offset in [-1, 1]:
            yy = y + offset
            if yy < 0 or yy >= self.height:
                continue
            if (x, yy) in seen:
                continue
            seen.update(self.fill(x, yy, seen))

        return seen


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
    basins = set()
    for y in range(grid.height):
        for x in range(grid.width):
            basin = grid.fill(x, y)
            if len(basin) == 0:
                continue
            basins.add(frozenset(basin))

    largest = [b for b in sorted(basins, key=len, reverse=True)]

    answer = 1
    for b in largest[:3]:
        answer *= len(b)

    return answer


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
