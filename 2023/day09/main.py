import fileinput


def score1(line):
    tri = [[int(n) for n in line.split()]]
    curr = tri[-1]
    while not all(n == 0 for n in curr):
        l = []
        for i in range(len(curr) - 1):
            l.append(curr[i+1] - curr[i])
        curr = l
        tri.append(curr)

    idx = len(tri) - 1
    tri[idx].append(0)
    idx -= 1

    while idx >= 0:
        tri[idx].append(tri[idx][-1] + tri[idx+1][-1])
        idx -= 1

#    for r in tri:
#        print(r)

    return tri[0][-1]


def score2(line):
    tri = [[int(n) for n in line.split()]]
    curr = tri[-1]
    while not all(n == 0 for n in curr):
        l = []
        for i in range(len(curr) - 1):
            l.append(curr[i+1] - curr[i])
        curr = l
        tri.append(curr)

    idx = len(tri) - 1
    tri[idx].insert(0, 0)
    idx -= 1

    while idx >= 0:
        tri[idx].insert(0, tri[idx][0] - tri[idx+1][0])
        idx -= 1

#    for r in tri:
#        print(r)

    return tri[0][0]


def part1(lines):
    return sum(score1(line) for line in lines)


def part2(lines):
    return sum(score2(line) for line in lines)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
