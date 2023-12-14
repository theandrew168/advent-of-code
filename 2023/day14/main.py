import fileinput
import itertools


class Grid:

    def __init__(self, lines):
        self.grid = [list(line) for line in lines]

    def dims(self):
        return len(self.grid[0]), len(self.grid)

    def score(self):
        total = 0

        w, h = self.dims()
        for y in range(h):
            s = self.slice(row=y)
            total += s.count('O') * (h - y)

        return total        

    def slice(self, col=None, row=None, rev=False):
        # ensure a copy is made
        if col is not None:
            s = [line[col] for line in self.grid]
            return list(reversed(s)) if rev else s
        if row is not None:
            s = [c for c in self.grid[row]]
            return list(reversed(s)) if rev else s

    def set_slice(self, s, col=None, row=None, rev=False):
        if col is not None:
            if rev:
                s = list(reversed(s))
            for i, c in enumerate(s):
                self.grid[i][col] = c
        if row is not None:
            if rev:
                s = list(reversed(s))
            self.grid[row] = s

    def shift(self, s):
        prev = 0
        block = 0
        while block < len(s):
            try:
                block = s.index('#', prev)
            except:
            # no more blocks, check up til end of slice
                block = len(s)

            # handle adjacent blocks
            if block - prev == 1:
                prev = block
                block += 1
                continue

            rocks = 'O' * s[prev:block].count('O')
            empty = '.' * s[prev:block].count('.')
            s[prev:block] = rocks + empty

            prev = block+1

    def tilt(self, d):
        w, h = self.dims()
        if d == 'N':
            for x in range(w):
                s = self.slice(col=x)
                self.shift(s)
                self.set_slice(s, col=x)
        elif d == 'S':
            for x in range(w):
                s = self.slice(col=x, rev=True)
                self.shift(s)
                self.set_slice(s, col=x, rev=True)
        elif d == 'W':
            for y in range(h):
                s = self.slice(row=y)
                self.shift(s)
                self.set_slice(s, row=y)
        elif d == 'E':
            for y in range(h):
                s = self.slice(row=y, rev=True)
                self.shift(s)
                self.set_slice(s, row=y, rev=True)

    def __str__(self):
        s = ''
        for line in self.grid:
            s += ''.join(line) + '\n'
        return s


def part1(lines):
    grid = Grid(lines)
    grid.tilt('N')
    return grid.score()


def part2(lines):
    grid = Grid(lines)

    seen = {}
    repeats = []

    cycle = 0
    while cycle < 200:
        cycle += 1
        for d in 'NWSE':
            grid.tilt(d)

        h = str(grid)
        if h in seen:
            repeats.append((cycle, seen[h][0], seen[h][1]))
        else:
            seen[h] = (cycle, grid.score())

    window = 5
    offset = repeats[0][0]
    period = None
    
    pattern = repeats[:window]
    for i in range(len(repeats)-window):
        chk = repeats[i:i+window]
        if [v[2] for v in chk] == [p[2] for p in pattern]:
            period = chk[0][0] - chk[0][1]
            break

    assert offset is not None
    assert period is not None

    index = (1_000_000_000 - offset) % period
    return repeats[index][2]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
