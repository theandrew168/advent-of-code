import fileinput
import functools


def parse(lines):
    have = lines[0].split(', ')
    want = lines[2:]
    return have, want


@functools.cache
def solve(have, design):
    if design == '':
        return 1

    total = 0
    for h in have:
        if design.startswith(h):
            total += solve(have, design[len(h):])
    return total


def part1(lines):
    have, want = parse(lines)
    have = tuple(sorted(have, key=len, reverse=True))

    total = 0
    for design in want:
        if solve(have, design):
            total += 1
    return total


def part2(lines):
    have, want = parse(lines)
    have = tuple(sorted(have, key=len, reverse=True))

    total = 0
    for design in want:
        total += solve(have, design)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
