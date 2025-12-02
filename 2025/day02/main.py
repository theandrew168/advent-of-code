import fileinput
import re

from more_itertools import chunked


def parse(lines):
    line = lines[0]

    rs = []
    for r in line.split(','):
        start, end = r.split('-')
        start = int(start)
        end = int(end)
        rs.append((start, end))
    return rs


def part1(lines):
    total = 0

    rs = parse(lines)
    for start, end in rs:
        for i in range(start, end+1):
            s = str(i)
            l = len(s)
            if l % 2 == 1:
                continue
            l //= 2
            if s[:l] == s[l:]:
                total += i

    return total


def part2(lines):
    total = 0

    rs = parse(lines)
    for start, end in rs:
        for i in range(start, end+1):
            s = str(i)
            l = len(s)
            for j in range(l//2 + 1):
                cs = [''.join(chunk) for chunk in chunked(s, j)]
                if len(set(cs)) == 1:
                    total += i
                    break

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
