import fileinput


def calc(n):
    s = n
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s


def part1(lines):
    total = 0
    for line in lines:
        s = int(line)
        for _ in range(2000):
            s = calc(s)
        total += s
    return total


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
