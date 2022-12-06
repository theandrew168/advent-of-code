import fileinput

from more_itertools import windowed


def part1(line):
    for i, window in enumerate(windowed(line, 4)):
        s = set(window)
        if len(s) == 4:
            return i + 4


def part2(line):
    for i, window in enumerate(windowed(line, 14)):
        s = set(window)
        if len(s) == 14:
            return i + 14


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines[0]))
    print(part2(lines[0]))
