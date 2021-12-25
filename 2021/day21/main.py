from collections import defaultdict
import fileinput
from functools import lru_cache
from itertools import cycle, islice, product


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


@lru_cache(maxsize=4096)
def apply_roll(p, s, r):
    p = (p + r) % 10
    s += p + 1
    return p, s


def play(op1, op2, os1, os2, uc, turn, hist):
    # base case: found a winner
    # loop: roll each option
    # recur: chosen option (zigzags between p1 and p2)

    w1, w2 = 0, 0
    if turn % 2 == 1:
        for roll, combos in hist.items():
            p1, s1 = apply_roll(op1, os1, roll)
            nuc = uc * len(combos)
            if s1 >= 21:
                w1 += nuc
            else:
                ww1, ww2 = play(p1, op2, s1, os2, nuc, turn + 1, hist)
                w1 += ww1
                w2 += ww2
    else:
        for roll, combos in hist.items():
            p2, s2 = apply_roll(op2, os2, roll)
            nuc = uc * len(combos)
            if s2 >= 21:
                w2 += nuc
            else:
                ww1, ww2 = play(op1, p2, os1, s2, nuc, turn + 1, hist)
                w1 += ww1
                w2 += ww2

    return w1, w2


# 3 1 [(1, 1, 1)]
# 4 3 [(1, 1, 2), (1, 2, 1), (2, 1, 1)]
# 5 6 [(1, 1, 3), (1, 2, 2), (1, 3, 1), (2, 1, 2), (2, 2, 1), (3, 1, 1)]
# 6 7 [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 2, 2), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
# 7 6 [(1, 3, 3), (2, 2, 3), (2, 3, 2), (3, 1, 3), (3, 2, 2), (3, 3, 1)]
# 8 3 [(2, 3, 3), (3, 2, 3), (3, 3, 2)]
# 9 1 [(3, 3, 3)]

def part2(op1, op2):
    rolls = [p for p in product(range(1, 4), range(1, 4), range(1, 4))]

    hist = defaultdict(list)
    for roll in rolls:
        hist[sum(roll)].append(roll)

    scores = play(op1, op2, 0, 0, 1, 1, hist)
    return max(scores)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    p1 = int(lines[0].split()[-1]) - 1
    p2 = int(lines[1].split()[-1]) - 1

    print(part1(p1, p2))
    print(part2(p1, p2))
