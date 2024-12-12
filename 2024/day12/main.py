from collections import defaultdict
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
            yield (xx, y)

        for yoff in [-1, 1]:
            yy = y + yoff
            yield (x, yy)

    def fill(self, x, y, seen):
        if (x, y) in seen:
            return seen

        new_seen = set(seen)
        new_seen.add((x, y))

        c = self.get(x, y)
        for xx, yy in self.adj4(x, y):
            if xx < 0 or xx >= self.width:
                continue
            if yy < 0 or yy >= self.height:
                continue
            if self.get(xx, yy) == c:
                new_seen |= self.fill(xx, yy, new_seen)

        return new_seen


def calc_regions(grid):
    # flood fill to determine regions
    regionID = 0
    regions = defaultdict(set)

    seen = set()
    for y in range(grid.height):
        for x in range(grid.width):
            fill = grid.fill(x, y, set())
            if fill & seen:
                continue
            regions[regionID] = fill
            regionID += 1
            seen |= fill

    return regions


def part1(lines):
    grid = Grid(lines)
    regions = calc_regions(grid)

    area = defaultdict(int)
    peri = defaultdict(int)
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid.get(x, y)

            r = None
            for k, v in regions.items():
                if (x, y) in v:
                    r = k
                    break
            area[r] += 1

            for xx, yy in grid.adj4(x, y):
                # check for edges
                if xx < 0 or xx >= grid.width:
                    peri[r] += 1
                    continue
                if yy < 0 or yy >= grid.height:
                    peri[r] += 1
                    continue
                # check if adj tile is different
                if grid.get(xx, yy) != c:
                    peri[r] += 1

    total = 0
    for r in regions:
        total += area[r] * peri[r]
    return total


def part2(lines):
    grid = Grid(lines)
    regions = calc_regions(grid)

    area = defaultdict(int)
    sides = defaultdict(set)
    for y in range(grid.height):
        for x in range(grid.width):
            c = grid.get(x, y)

            r = None
            for k, v in regions.items():
                if (x, y) in v:
                    r = k
                    break

            area[r] += 1
            for xx, yy in grid.adj4(x, y):
                side = None
                if xx < x:
                    side = (x, y, 'left')
                elif xx > x:
                    side = (x, y, 'right')
                elif yy < y:
                    side = (x, y, 'up')
                elif yy > y:
                    side = (x, y, 'down')

                assert side is not None

                # check for edges
                if xx < 0 or xx >= grid.width:
                    sides[r].add(side)
                    continue
                if yy < 0 or yy >= grid.height:
                    sides[r].add(side)
                    continue
                # check if adj tile is different
                if grid.get(xx, yy) != c:
                    sides[r].add(side)

    total = 0
    for r in regions:
        ss = defaultdict(set)

        # group edges by axis
        for x, y, d in sides[r]:
            if d in ['up', 'down']:
                ss[(y, d)].add((x, y, d))
            else:
                ss[(x, d)].add((x, y, d))

        # count gaps (extra edges)
        side_count = len(ss)
        for k, v in ss.items():
            if k[1] in ['up', 'down']:
                # check for gaps along X axis
                xs = sorted(vv[0] for vv in v)
                curr = xs[0]
                for check in xs:
                    if check - curr > 1:
                        side_count += 1
                    curr = check
            else:
                # check for gaps along Y axis
                ys = sorted(vv[1] for vv in v)
                curr = ys[0]
                for check in ys:
                    if check - curr > 1:
                        side_count += 1
                    curr = check

        total += area[r] * side_count

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
