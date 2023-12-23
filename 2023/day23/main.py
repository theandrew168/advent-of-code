import fileinput

import sys
sys.setrecursionlimit(100000)


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def get(self, pt):
        x, y = pt
        return self.lines[y][x]

    def adj(self, pt):
        x, y = pt
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


def longest_path(grid, pt, seen, path, part2=False):
    seen.add(pt)

    edges = []

    c = grid.get(pt)
    if c == '.' or part2:
        # normal tile, find adj that are not walls
        for adj in grid.adj(pt):
            if grid.get(adj) == '#':
                continue
            edges.append(adj)
    else:
        # slope tile, only adj is the slope direction
        adj = [pt[0], pt[1]]
        if c == '^':
            adj[1] -= 1
        elif c == 'v':
            adj[1] += 1
        elif c == '<':
            adj[0] -= 1
        elif c == '>':
            adj[0] += 1
        else:
            assert False
        edges.append(tuple(adj))

    paths = []
    for edge in edges:
        if edge in seen:
            continue
        new_path = path + [edge]
        paths.append(tuple(new_path))
        paths.extend(longest_path(grid, edge, set(seen), new_path, part2))

    return paths


def pretty(grid, path):
    s = ''
    for y in range(grid.height):
        row = ''
        for x in range(grid.width):
            pt = (x, y)
            c = 'O' if pt in path else grid.get(pt)
            row += c
        s += row + '\n'
    return s


def part1(lines):
    grid = Grid(lines)
    start = (1,0)
    end = (grid.width-2, grid.height-1)
    paths = longest_path(grid, start, set(), [])
    max_len = max(len(p) for p in paths if p[-1] == end)
    return max_len


def part2(lines):
    grid = Grid(lines)
    start = (1,0)
    end = (grid.width-2, grid.height-1)
    paths = longest_path(grid, start, set(), [], True)
    max_len = max(len(p) for p in paths if p[-1] == end)
    return max_len


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
