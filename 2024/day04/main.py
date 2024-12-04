import fileinput
import re


def rows(lines):
    for line in lines:
        yield line


def cols(lines):
    width = len(lines[0])
    for x in range(width):
        col = []
        for line in lines:
            col.append(line[x])
        yield ''.join(col)


def diag_forward(lines):
    width = len(lines[0])
    height = len(lines)

    # y-axis first
    for i in range(height):
        diag = []
        x = 0
        y = i
        while y >= 0:
            diag.append(lines[y][x])
            y -= 1
            x += 1 
        yield ''.join(diag)

    # then the x-axis
    for i in range(1, width):
        diag = []
        x = i
        y = height - 1
        while x < width:
            diag.append(lines[y][x])
            y -= 1
            x += 1
        yield ''.join(diag)


def diag_backward(lines):
    width = len(lines[0])
    height = len(lines)

    # y-axis first
    for i in range(height):
        diag = []
        x = width - 1
        y = i
        while y >= 0:
            diag.append(lines[y][x])
            y -= 1
            x -= 1 
        yield ''.join(diag)

    # then the x-axis
    for i in range(width-2, -1, -1):
        diag = []
        x = i
        y = height - 1
        while x >= 0:
            diag.append(lines[y][x])
            y -= 1
            x -= 1
        yield ''.join(diag)


def squares(lines):
    width = len(lines[0])
    height = len(lines)

    for y in range(height-2):
        for x in range(width-2):
            square = []
            for yy in range(y, y+3):
                row = []
                for xx in range(x, x+3):
                    row.append(lines[yy][xx])
                square.append(row)
            yield square


def part1(lines):
    pat = re.compile(r'(?=XMAS|SAMX)')

    total = 0
    for line in rows(lines):
        matches = pat.findall(line)
        total += len(matches)
    for line in cols(lines):
        matches = pat.findall(line)
        total += len(matches)
    for line in diag_forward(lines):
        matches = pat.findall(line)
        total += len(matches)
    for line in diag_backward(lines):
        matches = pat.findall(line)
        total += len(matches)
    return total


def part2(lines):
    total = 0
    # row-major, origin in upper left
    for s in squares(lines):
        # verify center is A
        if s[1][1] != 'A':
            continue
        # four other variations to check:
        # top-left            top-right          bottom-left        bottom-right
        if s[0][0] == 'M' and s[0][2] == 'M' and s[2][0] == 'S' and s[2][2] == 'S':
            total += 1
        if s[0][0] == 'S' and s[0][2] == 'S' and s[2][0] == 'M' and s[2][2] == 'M':
            total += 1
        if s[0][0] == 'M' and s[0][2] == 'S' and s[2][0] == 'M' and s[2][2] == 'S':
            total += 1
        if s[0][0] == 'S' and s[0][2] == 'M' and s[2][0] == 'S' and s[2][2] == 'M':
            total += 1
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
