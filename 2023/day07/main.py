from collections import Counter
import fileinput
from functools import cmp_to_key

STR1 = '23456789TJQKA'
STR2 = 'J23456789TQKA'


def score1(hand):
    c = Counter(hand)

    (_, a), = c.most_common(1)
    if a == 5:
        return 6 #'five'
    if a == 4:
        return 5 #'four'
    
    (_, a), (_, b) = c.most_common(2)
    if a == 3 and b == 2:
        return 4 #'full'
    if a == 3:
        return 3 #'three'
    if a == 2 and b == 2:
        return 2 #'tpair'
    if a == 2:
        return 1 #'pair'

    return 0 #'high'


def cmp1(a, b):
    sa, sb = score1(a), score1(b)
    if sa == sb:
        va = [STR1.index(v) for v in a]
        vb = [STR1.index(v) for v in b]
        if va == vb:
            return 0
        if va < vb:
            return -1
        if va > vb:
            return 1

    return sa - sb


def score2(hand):
    c = Counter(hand)
    js = c['J']
    if js == 5 or js == 4:
        return 6  #'five'

    # three or fewer Js at this point

    (_, a), = c.most_common(1)
    if a == 5:
        return 6 #'five'

    (ach, a), (bch, b) = c.most_common(2)
    if a == 4:
        if ach == 'J' or bch == 'J':
            return 6#'five'
        else:
            return 5 #'four'

    if a == 3 and b == 2:
        if ach == 'J' or bch == 'J':
            return 6 # five
        else:
            return 4 #'full'

    if a == 3:
        if ach == 'J' or js == 1:
            return 5 # four
        return 3 #'three'

    if a == 2 and b == 2:
        if ach == 'J' or bch == 'J':
            return 5 # four
        if js == 1:
            return 4 # full
        return 2 #'tpair'

    if a == 2:
        if ach == 'J' or js == 1:
            return 3
        return 1 #'pair'

    if js == 1:
        return 1

    return 0


def cmp2(a, b):
    sa, sb = score2(a), score2(b)
    if sa == sb:
        va = [STR2.index(v) for v in a]
        vb = [STR2.index(v) for v in b]
        if va == vb:
            return 0
        if va < vb:
            return -1
        if va > vb:
            return 1

    return sa - sb


def part1(lines):
    hands = []
    for line in lines:
        hand, bid = line.split()
        bid = int(bid)
        hands.append((hand, bid))

    hands = sorted(hands, key=lambda hand: cmp_to_key(cmp1)(hand[0]))

    total = 0
    for i, (hand, bid) in enumerate(hands, start=1):
        total += i * bid

    return total


def part2(lines):
    hands = []
    for line in lines:
        hand, bid = line.split()
        bid = int(bid)
        hands.append((hand, bid))

    hands = sorted(hands, key=lambda hand: cmp_to_key(cmp2)(hand[0]))

    total = 0
    for i, (hand, bid) in enumerate(hands, start=1):
        total += i * bid

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
