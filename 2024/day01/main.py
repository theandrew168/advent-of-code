from collections import Counter
import fileinput


def part1(lines):
    pairs = [line.split() for line in lines]
    left = sorted(int(pair[0]) for pair in pairs)
    right = sorted(int(pair[1]) for pair in pairs)

    total = 0
    for l, r in zip(left, right):
        total += abs(l - r)
    return total


def part2(lines):
    pairs = [line.split() for line in lines]
    left = sorted(int(pair[0]) for pair in pairs)
    right = sorted(int(pair[1]) for pair in pairs)
    c = Counter(right)

    total = 0
    for n in left:
        total += n * c[n]
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
