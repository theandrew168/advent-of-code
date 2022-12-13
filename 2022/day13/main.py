import fileinput
from functools import cmp_to_key
from itertools import zip_longest

from more_itertools import split_at


class Pass(Exception):
    pass


class Fail(Exception):
    pass


def check(a, b):
    # base case, no more to compare, good to go
    if not a and not b:
        return

    # compare each pair of elements
    for aa, bb in zip_longest(a, b):
        # left side ran out
        if aa is None:
            raise Pass()

        # right side ran out
        if bb is None:
            raise Fail()

        ta, tb = type(aa), type(bb)

        # both ints, simple compare
        if ta == int and tb == int:
            if aa < bb:
                raise Pass()
            elif aa > bb:
                raise Fail()
            else:
                continue

        aa = [aa] if ta == int else aa
        bb = [bb] if tb == int else bb
        check(aa, bb)


def compare(a, b):
    try:
        check(a, b)
    except Pass:
        return 1
    except Fail:
        return -1


def part1(lines):
    score = 0

    pairs = split_at(lines, lambda x: x == '')
    for i, [a, b] in enumerate(pairs, start=1):
        a, b = eval(a), eval(b)
        c = compare(a, b)
        if c > 0:
            score += i

    return score


def part2(lines):
    lines = [line for line in lines if line]
    lines.append('[[2]]')
    lines.append('[[6]]')
    lines = [eval(line) for line in lines]

    lines = reversed(sorted(lines, key=cmp_to_key(compare)))
    lines = list(lines)
    idx_a = lines.index([[2]]) + 1
    idx_b = lines.index([[6]]) + 1

    return idx_a * idx_b


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
