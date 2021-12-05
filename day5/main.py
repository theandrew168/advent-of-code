import fileinput


class Grid:

    def __init__(self, size=1000):
        self.size = size
        self.grid = [0] * size * size

    def __str__(self):
        s = ''
        for y in range(10):
            line = ''
            for x in range(10):
                idx = self.index(x, y)
                line += str(self.grid[idx])
            s += line + '\n'
        return s

    def index(self, x, y):
        return (y * self.size) + x

    def mark(self, x, y):
        idx = self.index(x, y)
        self.grid[idx] += 1

    def draw(self, x1, y1, x2, y2, diag=False):
        # vertical
        if x1 == x2:
            start = min(y1, y2)
            end = max(y1, y2) + 1  # includes both ends
            for y in range(start, end):
                self.mark(x1, y)
            return

        # horizontal
        if y1 == y2:
            start = min(x1, x2)
            end = max(x1, x2) + 1  # includes both ends
            for x in range(start, end):
                self.mark(x, y1)
            return

        # diagonal
        if not diag:
            return

        # determine starting x
        if x1 < x2:
            start = (x1, y1)
            end = (x2, y2)
        else:
            start = (x2, y2)
            end = (x1, y1)

        # determine y step (up or down)
        if start[1] < end[1]:
            step = 1
        else:
            step = -1

        # draw!
        y = start[1]
        for x in range(start[0], end[0] + 1):
            self.mark(x, y)
            y += step

    def score(self):
        return sum(1 for p in self.grid if p >= 2)


def part1(segments):
    grid = Grid()
    for s in segments:
        grid.draw(*s)
    return grid.score()


def part2(segments):
    grid = Grid()
    for s in segments:
        grid.draw(*s, diag=True)
    return grid.score()


if __name__ == '__main__':
    segments = []
    for line in fileinput.input():
        a, _, b = line.strip().split()
        x1, y1 = a.split(',')
        x2, y2 = b.split(',')
        segment = (int(x1), int(y1), int(x2), int(y2))
        segments.append(segment)

    print(part1(segments))
    print(part2(segments))
