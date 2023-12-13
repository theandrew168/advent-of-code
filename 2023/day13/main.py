import fileinput

# > 28580


def split(lines):
    pattern = []
    for line in lines:
        if len(line) == 0:
            yield pattern
            pattern = []
        else:
            pattern.append(line)

    yield pattern


def row(pattern, y):
    return pattern[y]


def col(pattern, x):
    return ''.join(r[x] for r in pattern)


def dist(a,b):
    return sum(0 if a[i] == b[i] else 1 for i in range(len(a)))


def part1(lines):
    patterns = list(split(lines))

    total = 0
    for pattern in patterns:
        w = len(pattern[0])
        h = len(pattern)

        # check cols
        for x in range(w-1):
            if col(pattern, x) == col(pattern, x + 1):
#                print('col at {},{}'.format(x, x+1))
                valid = True
                x0, x1 = x, x+1
                while True:
                    x0 -= 1
                    x1 += 1
                    if x0 < 0 or x1 >= w:
                        break
                    if col(pattern, x0) != col(pattern, x1):
                        valid = False
                        break
#                print('valid?', valid)
                if valid:
                    total += x+1

        # check rows
        for y in range(h-1):
            if row(pattern, y) == row(pattern, y + 1):
#                print('row at {},{}'.format(y, y+1))
                valid = True
                y0, y1 = y, y+1
                while True:
                    y0 -= 1
                    y1 += 1
                    if y0 < 0 or y1 >= h:
                        break
                    if row(pattern, y0) != row(pattern, y1):
                        valid = False
                        break
#                print('valid?', valid)
                if valid:
                    total += 100 * (y+1)

    return total


def part2(lines):
    patterns = list(split(lines))

    total = 0
    for pattern in patterns:
        w = len(pattern[0])
        h = len(pattern)

        # check cols
        for x in range(w-1):
            smudge = False
            d = dist(col(pattern, x), col(pattern,x+1))
            if col(pattern, x) == col(pattern, x + 1) or d == 1:
                if d == 1:
                    smudge = True
#                print('col at {},{}'.format(x, x+1))
                valid = True
                x0, x1 = x, x+1
                while True:
                    x0 -= 1
                    x1 += 1
                    if x0 < 0 or x1 >= w:
                        break
                    d = dist(col(pattern, x0), col(pattern, x1))
                    if col(pattern, x0) != col(pattern, x1):
                        if d == 1 and not smudge:
                            smudge = True
                            continue
                        valid = False
                        break
#                print('valid?', valid)
                if valid and smudge:
                    total += x+1

        # check rows
        for y in range(h-1):
            smudge = False
            d = dist(row(pattern, y), row(pattern, y+1))
            if row(pattern, y) == row(pattern, y + 1) or d == 1:
                if d == 1:
                    smudge = True
#                print('row at {},{}'.format(y, y+1))
                valid = True
                y0, y1 = y, y+1
                while True:
                    y0 -= 1
                    y1 += 1
                    if y0 < 0 or y1 >= h:
                        break
                    d = dist(row(pattern, y0), row(pattern, y1))
                    if row(pattern, y0) != row(pattern, y1):
                        if d == 1 and not smudge:
                            smudge = True
                            continue
                        valid = False
                        break
#                print('valid?', valid)
                if valid and smudge:
                    total += 100 * (y+1)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
