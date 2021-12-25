import fileinput


class Grid:

    def __init__(self, data, width=10, height=10):
        self.data = data
        self.width = width
        self.height = height

    def __str__(self):
        s = ''
        for y in range(self.height):
            start = y * self.width
            end = start + self.width
            row = self.data[start:end]
            line = ' '.join('{:2d}'.format(n) for n in row)
            s += line + '\n'

        return s

    def __len__(self):
        return len(self.data)

    def idx(self, x, y):
        return y * self.width + x

    def adj(self, x, y):
        for yoff in [-1, 0, 1]:
            for xoff in [-1, 0, 1]:
                xx, yy = x + xoff, y + yoff
                # skip self
                if xx == x and yy == y:
                    continue
                # skip x OOB
                if xx < 0 or xx >= self.width:
                    continue
                # skip y OOB
                if yy < 0 or yy >= self.height:
                    continue

                yield (xx, yy)

    def step(self):
        # increase each cell by 1
        after = [c + 1 for c in self.data]

        # resolve flashes
        flashes = set()
        while any(n > 9 for n in after):
            for y in range(self.height):
                for x in range(self.width):
                    idx = self.idx(x, y)

                    # doesn't need to flash
                    if after[idx] <= 9:
                        continue

                    # already flashed
                    if (x, y) in flashes:
                        continue

                    # lets flash!
                    after[idx] = 0
                    flashes.add((x, y))

                    # inc adjacent (if not flashed)
                    for xadj, yadj in self.adj(x, y):
                        if (xadj, yadj) in flashes:
                            continue
                        after[self.idx(xadj, yadj)] += 1

        self.data = after
        return len(flashes)


def part1(grid):
    return sum(grid.step() for _ in range(100))


def part2(grid):
    i = 0
    while True:
        i += 1
        flashes = grid.step()
        if flashes == len(grid):
            return i


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    width = len(lines[0])
    height = len(lines)
    data = [int(n) for n in ''.join(lines)]

    print(part1(Grid(data, width, height)))
    print(part2(Grid(data, width, height)))
