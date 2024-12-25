import fileinput


def split(lines):
    schematic = []
    for line in lines:
        if not line:
            yield schematic
            schematic = []
        else:
            schematic.append(line)
    yield schematic


def parse(lines):
    locks = []
    keys = []

    for s in split(lines):
        pins = [-1] * 5
        w = len(s[0])
        h = len(s)
        for x in range(w):
            for y in range(h):
                if s[y][x] == '#':
                    pins[x] += 1

        if s[0][0] == '#':
            locks.append(pins)
        else:
            keys.append(pins)

    return locks, keys


def part1(lines):
    locks, keys = parse(lines)

    total = 0
    for lock in locks:
        for key in keys:
            pins = [lock[i] + key[i] for i in range(5)]
            if all(pin <= 5 for pin in pins):
                total += 1
    return total


def part2(lines):
    return 'Merry Christmas! See you all in 2025!'


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
