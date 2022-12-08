import fileinput
import math


class Grid:

    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)

        # row-major
        self.grid = [int(n) for n in ''.join(lines)]

    def __str__(self):
        s = ''
        for y in range(self.height):
            idx = y * self.width
            s += str(self.grid[idx:idx+self.width]) + '\n'

        return s

    def get(self, x, y):
        idx = (y * self.width) + x
        return self.grid[idx]

    def row(self, y):
        start = y * self.width
        end = start + self.width
        return self.grid[start:end]

    def col(self, x):
        step = self.width
        return self.grid[x::self.width]

    def visible(self, x, y):
        if x <= 0 or x >= self.width - 1:
            return True
        if y <= 0 or y >= self.height - 1:
            return True

        row = self.row(y)
        row_before, row_after = row[:x], row[x+1:]

        col = self.col(x)
        col_before, col_after = col[:y], col[y+1:]
 
        tree = self.get(x, y)
        views = [row_before, row_after, col_before, col_after]
        return any(tree > max(view) for view in views)

    def view_dist(self, tree, view):
        dist = 0
        for t in view:
            dist += 1
            if t >= tree:
                return dist

        return dist

    def scenic(self, x, y):
        tree = self.get(x, y)

        row = self.row(y)
        row_before, row_after = reversed(row[:x]), row[x+1:]

        col = self.col(x)
        col_before, col_after = reversed(col[:y]), col[y+1:]
 
        views = [row_before, row_after, col_before, col_after]
        dists = [self.view_dist(tree, view) for view in views]
        return dists


def part1(lines):
    grid = Grid(lines)

    score = 0
    for y in range(grid.height):
        for x in range(grid.width):
            score += grid.visible(x, y)

    return score


def part2(lines):
    grid = Grid(lines)

    best = 0
    for y in range(grid.height):
        for x in range(grid.width):
            score = math.prod(grid.scenic(x, y))
            if score > best:
                best = score

    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
