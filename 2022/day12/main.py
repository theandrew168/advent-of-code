import fileinput

from more_itertools import grouper


class Grid:

    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
        self.grid = ''.join(lines)

        start = self.grid.index('S')
        self.start = (start % self.width, start // self.width)

        end = self.grid.index('E')
        self.end= (end % self.width, end // self.width)

        self.grid = self.grid.replace('S', 'a')
        self.grid = self.grid.replace('E', 'z')

    def __str__(self):
        s = ''
        for line in grouper(self.grid, self.width):
            s += ''.join(line) + '\n'
        return s

    def get(self, x, y):
        idx = (y * self.width) + x
        return self.grid[idx]

    def adj(self, x, y, skip):
        cur = self.get(x, y)
        for dx in [-1, 1]:
            x1 = x + dx
            if x1 < 0 or x1 >= self.width:
                continue

            step = self.get(x1, y)
            if skip(ord(step) - ord(cur)):
                continue
            yield x1, y

        for dy in [-1, 1]:
            y1 = y + dy
            if y1 < 0 or y1 >= self.height:
                continue

            step = self.get(x, y1)
            if skip(ord(step) - ord(cur)):
                continue
            yield x, y1


def part1(lines):
    grid = Grid(lines)

    visited = {grid.start: 0}
    queue = [grid.start]
    while queue:
        p = queue.pop(0)
        for n in grid.adj(p[0], p[1], lambda x: x > 1):
            if n in visited:
                continue
            visited[n] = visited[p] + 1
            queue.append(n)

    return visited[grid.end]


def part2(lines):
    grid = Grid(lines)

    visited = {grid.end: 0}
    queue = [grid.end]
    while queue:
        p = queue.pop(0)
        for n in grid.adj(p[0], p[1], lambda x: x < -1):
            if n in visited:
                continue
            visited[n] = visited[p] + 1
            queue.append(n)

    return min(v for k, v in visited.items() if grid.get(k[0], k[1]) == 'a')


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
