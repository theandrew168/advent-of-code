import fileinput


def find_start_end(lines):
    width = len(lines[0])
    height = len(lines)

    start = None
    end = None
    for y in range(height):
        for x in range(width):
            c = lines[y][x]
            if c == 'S':
                start = (x, y)
            if c == 'E':
                end = (x, y)

    return start, end


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start, end = find_start_end(lines)
    print(start, end)
    pass


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
