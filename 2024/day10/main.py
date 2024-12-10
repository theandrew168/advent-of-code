import fileinput


class Grid:
    def __init__(self, lines):
        self._lines = lines
        self._width = len(lines[0])
        self._height = len(lines)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get(self, x, y):
        return self._lines[y][x]

    def adj4(self, x, y):
        for xoff in [-1, 1]:
            xx = x + xoff
            if xx < 0 or xx >= self.width:
                continue

            yield (xx, y)

        for yoff in [-1, 1]:
            yy = y + yoff
            if yy < 0 or yy >= self.height:
                continue

            yield (x, yy)


def search(grid, path):
    pos = path[-1]
    ele = grid.get(*pos)
    if ele == '9':
        yield path
    else:
        for adj in grid.adj4(*pos):
            ae = grid.get(*adj)
            if int(ae) == int(ele) + 1:
                yield from search(grid, path + [adj])


def part1(lines):
    grid = Grid(lines)

    trailheads = []
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid.get(x, y)
            if c == '0':
                trailheads.append((x, y))

    
    total = 0
    for t in trailheads:
        score = set()
        for path in search(grid, [t]):
            score.add(list(path)[-1])
        total += len(score)
    return total


def part2(lines):
    grid = Grid(lines)

    trailheads = []
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid.get(x, y)
            if c == '0':
                trailheads.append((x, y))

    
    total = 0
    for t in trailheads:
        paths = search(grid, [t])
        total += len(list(paths))
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
