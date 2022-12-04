import fileinput


def part1(lines):
    score = 0
    for line in lines:
        a, b = line.split(',')
        a0, a1 = a.split('-')
        b0, b1 = b.split('-')
        a, b = range(int(a0), int(a1)+1), range(int(b0), int(b1)+1)
        a, b = set(a), set(b)
        if a <= b or b <= a:
            score += 1
    return score


def part2(lines):
    score = 0
    for line in lines:
        a, b = line.split(',')
        a0, a1 = a.split('-')
        b0, b1 = b.split('-')
        a, b = range(int(a0), int(a1)+1), range(int(b0), int(b1)+1)
        a, b = set(a), set(b)
        if a & b:
            score += 1
    return score


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
