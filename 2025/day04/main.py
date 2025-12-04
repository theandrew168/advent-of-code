import fileinput


def adj8(grid, w, h, x, y):
    adj = []

    for yoff in [-1, 0, 1]:
        yy = y + yoff
        for xoff in [-1, 0, 1]:
            xx = x + xoff

            # skip self
            if yoff == 0 and xoff == 0:
                continue

            # skip OOB (vert)
            if yy < 0 or yy >= h:
                continue

            # skip OOB (horiz)
            if xx < 0 or xx >= w:
                continue

            adj.append(grid[yy][xx])

    return adj


def part1(lines):
    grid = [list(line) for line in lines]
    w = len(grid[0])
    h = len(grid)

    total = 0
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if c != '@':
                continue

            adj = adj8(grid, w, h, x, y)
            cnt = len(list(c for c in adj if c == '@'))
            if cnt < 4:
                total += 1

    return total


def part2(lines):
    grid = [list(line) for line in lines]
    w = len(grid[0])
    h = len(grid)

    total = 0
    rolls = []
    while total == 0 or rolls:
        total += len(rolls)
        for x, y in rolls:
            grid[y][x] = '.'
        rolls = []

        for y in range(h):
            for x in range(w):
                c = grid[y][x]
                if c != '@':
                    continue

                adj = adj8(grid, w, h, x, y)
                cnt = len(list(c for c in adj if c == '@'))
                if cnt < 4:
                    rolls.append((x, y))

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
