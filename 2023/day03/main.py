from collections import namedtuple
import fileinput
import math
import re


Part = namedtuple('Part', 'number line start end')
Symbol = namedtuple('Symbol', 'value x y')


def parse_parts(lines):
    for i, line in enumerate(lines):
        matches = re.finditer(r'\d+', line.strip())
        for m in matches:
            part = Part(int(m.group(0)), i, m.start(), m.end()-1)
            yield part


def parse_symbols(lines):
    for i, line in enumerate(lines):
        matches = re.finditer(r'[^0-9\.]', line.strip())
        for m in matches:
            symbol = Symbol(m.group(0), m.start(), i)
            yield symbol


def part1(lines):
    parts = list(parse_parts(lines))
    symbols = list(parse_symbols(lines))

    total = 0
    for p in parts:
        for s in symbols:
            ds = math.dist([p.start, p.line], [s.x, s.y])
            de = math.dist([p.end, p.line], [s.x, s.y])
            if ds < 2 or de < 2:
                total += p.number
                break

    return total


def part2(lines):
    parts = list(parse_parts(lines))
    symbols = list(parse_symbols(lines))

    total = 0
    for s in symbols:
        if s.value != '*':
            continue

        gears = []
        for p in parts:
            ds = math.dist([p.start, p.line], [s.x, s.y])
            de = math.dist([p.end, p.line], [s.x, s.y])
            if ds < 2 or de < 2:
                gears.append(p)

        if len(gears) == 2:
            total += gears[0].number * gears[1].number

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
