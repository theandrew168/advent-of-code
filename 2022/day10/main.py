import fileinput

from more_itertools import grouper


def part1(lines):
    signals = []
    checks = set(range(20, 10000, 40))

    x = 1
    cycle = 0
    for line in lines:
        line = line.split()

        # noop
        if len(line) == 1:
            cycle += 1
            if cycle in checks:
                signals.append(cycle * x)
            continue

        # addx (first cycle)
        cycle += 1
        if cycle in checks:
            signals.append(cycle * x)

        # addx (second cycle)
        cycle += 1
        if cycle in checks:
            signals.append(cycle * x)

        # addx
        n = int(line[1])
        x += n

    return sum(signals)


def part2(lines):
    pixels = ['.'] * 240

    x = 1
    cycle = 0
    sprite = [x - 1, x, x + 1]

    def draw():
        pos = cycle - 1
        if pos % 40 in sprite:
            pixels[pos] = '#'

    for line in lines:
        line = line.split()

        # noop
        if len(line) == 1:
            cycle += 1
            draw()
            continue

        # addx (first cycle)
        cycle += 1
        draw()

        # addx (second cycle)
        cycle += 1
        draw()

        # addx
        n = int(line[1])
        x += n
        sprite = [x - 1, x, x + 1]

    return '\n'.join(''.join(g) for g in grouper(pixels, 40))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
