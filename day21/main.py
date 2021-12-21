from collections import defaultdict
import fileinput
from itertools import cycle, islice, permutations, product


def part1(op1, op2):
    d100 = cycle(range(1, 101))
    dc = 0

    p1, p2 = op1, op2
    s1, s2 = 0, 0
    while True:
        dc += 3
        p1 = (p1 + sum(islice(d100, 3))) % 10
        s1 += p1 + 1
        if s1 >= 1000:
            break

        dc += 3
        p2 = (p2 + sum(islice(d100, 3))) % 10
        s2 += p2 + 1
        if s2 >= 1000:
            break

    return min(s1, s2) * dc


def setp(d, i):
    if len(i) == 1:
        d[i[0]] = None
    else:
        if i[0] not in d:
            d[i[0]] = {}
        setp(d[i[0]], i[1:])


def ucount(d, hist, depth=27):
    if d is None:
        return 0

    uc = 0
    for k in d:
        uc += len(hist[k]) * depth

    for k, sub in d.items():
        uc += len(hist[k]) * ucount(sub, hist, depth * 27)

    return uc


def part2(op1, op2):
    rolls = [p for p in product(range(1, 4), range(1, 4), range(1, 4))]

    c = defaultdict(list)
    for roll in rolls:
        c[sum(roll)].append(roll)

    outcomes = list(c)
    perms = permutations(outcomes)

    w1, w2 = set(), set()
    for perm in perms:
        p1, p2 = op1, op2
        s1, s2 = 0, 0

        for i, p in enumerate(perm):
            p1 = (p1 + p) % 10
            s1 += p1 + 1
            if s1 >= 21:
                w1.add(perm[:i + 1])
                break

            p2 = (p2 + p) % 10
            s2 += p2 + 1
            if s2 >= 21:
                w2.add(perm[:i + 1])
                break

    for k, v in c.items():
        print(k, v)

    print(w1)
    print(w2)

    d = {}
    for w in w1:
        setp(d, w)
    print(d)
    for k, v in d.items():
        print(k, v)
    print(ucount(d, c))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    p1 = int(lines[0].split()[-1]) - 1
    p2 = int(lines[1].split()[-1]) - 1

    print(part1(p1, p2))
    print(part2(p1, p2))
