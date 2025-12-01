import fileinput


def part1(lines):
    total = 0

    cur = 50
    for line in lines:
        d, n = line[0], int(line[1:])
        if d == 'L':
            cur -= n
        else:
            cur += n

        cur %= 100
        if cur == 0:
            total += 1

    return total


def part2(lines):
    total = 0

    cur = 50
    for line in lines:
        isAtZero = cur == 0
        d, n = line[0], int(line[1:])

        rot = n // 100
        rem = n % 100

        total += rot
        if rem == 0:
            continue

        if d == 'L':
            cur -= rem
            if cur <= 0 and not isAtZero:
                total += 1
        else:
            cur += rem
            if cur >= 100 and not isAtZero:
                total += 1

        cur %= 100

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
