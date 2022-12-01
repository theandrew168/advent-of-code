from more_itertools import split_at

import fileinput


def part1(lines):
    foods = list(split_at(lines, lambda x: x == ''))
    cals = [sum(int(n) for n in food) for food in foods]
    return max(cals)

def part2(lines):
    foods = list(split_at(lines, lambda x: x == ''))
    cals = [sum(int(n) for n in food) for food in foods]
    most = list(reversed(sorted(cals)))
    return sum(most[:3])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
