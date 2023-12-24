import fileinput


def parse(lines):
    for line in lines:
        pos, vel = line.split('@')
        pos = pos.strip()
        vel = vel.strip()
        pos = tuple(int(n) for n in pos.split(', '))
        vel = tuple(int(n) for n in vel.split(', '))
        yield pos, vel


def part1(lines):
    for p,v in parse(lines):
        print(p,v)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
