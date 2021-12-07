import fileinput


def summation(n):
    return (n*n + n) / 2


def fuel_linear(positions, i):
    return int(sum(abs(p - i) for p in positions))


def fuel_summation(positions, i):
    return int(sum(summation(abs(p - i)) for p in positions))


def part1(positions):
    mn = min(positions)
    mx = max(positions)

    lowest = None
    for i in range(mn, mx + 1):
        fuel = fuel_linear(positions, i)
        if not lowest or fuel < lowest:
            lowest = fuel

    return lowest


def part2(positions):
    mn = min(positions)
    mx = max(positions)

    lowest = None
    for i in range(mn, mx + 1):
        fuel = fuel_summation(positions, i)
        if not lowest or fuel < lowest:
            lowest = fuel

    return lowest


if __name__ == '__main__':
    positions = None
    for line in fileinput.input():
        positions = [int(n) for n in line.strip().split(',')]
        break

    print(part1(positions))
    print(part2(positions))
