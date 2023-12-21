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

    def get2(self, pt):
        x, y = pt
        x = x % self.w
        y = y % self.h
        return self.lines[y][x]

    def adj2(self, pt):
        x, y = pt
        for yoff in [-1, 1]:
            yy = y + yoff
            yield x, yy
        for xoff in [-1, 1]:
            xx = x + xoff
            yield xx, y


def find_start(grid):
    for y in range(grid.h):
        for x in range(grid.w):
            pt = (x, y)
            if grid.get(pt) == 'S':
                return pt
    assert False


def expand(lines, by=1):
    new_lines = []
    for _ in range(3):
        for line in lines:
            new_lines.append(line * 3)
    return new_lines


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


# 1x1 map
# curr 7423 129
# curr 7434 130 <- stabilizes
# curr 7427 131 <- edge
# curr 7434 132
# curr 7427 133

# 3x3 map
# curr 66878 654
# curr 66871 655 <- stabilizes
# curr 66878 656
# curr 66871 657
# curr 66878 658
# curr 66871 659


# samples at: (n-65) % 131 == 0
# 65,3791
# 196,33646
# 327,93223
# 458,182522

# wolfram yields formula:
# 14861n^2 - 14728n + 3658
def quad(n):
    n = (n-65) / 131
    n += 1
    return int(14861*n*n - 14728*n + 3658)


def part2(lines):
    grid = Grid(lines)
    start = find_start(grid)

#    for n in [65,196,327,458,26501365]:
#        print(quad(n))
    return quad(26501365)

    # used to generate a sample series
    curr = set()
    curr.add(start)
    for i in range(1000):
        nxt = set()
        for pt in curr:
            for adj in grid.adj2(pt):
                c = grid.get2(adj)
                if c == '#':
                    continue
                nxt.add(adj)
        curr = nxt
        step = i+1
        if (step-65) % 131 == 0: 
            print('{},{}'.format(step, len(curr)))

    return len(curr)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
