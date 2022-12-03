import fileinput

from more_itertools import grouper


def s(c):
    if c.islower():
        return ord(c) - 96
    else:
        return ord(c) - 38


def part1(lines):
    score = 0
    for line in lines:
        half = int(len(line) / 2)
        a, b = line[:half], line[half:]
        inter = set(a) & set(b)
        score += s(inter.pop())
    return score


def part2(lines):
    score = 0
    for group in grouper(lines, 3):
        a, b, c = group
        inter = set(a) & set(b) & set(c)
        score += s(inter.pop())
    return score


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
