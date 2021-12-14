from collections import Counter, defaultdict
import fileinput

from more_itertools import sliding_window


class List:

    def __init__(self, value, link=None):
        self.value = value
        self.link = link

    def __str__(self):
        s = ''
        ptr = self
        while ptr is not None:
            s += ptr.value
            ptr = ptr.link
        return s

    def __len__(self):
        size = 0
        ptr = self
        while ptr is not None:
            size += 1
            ptr = ptr.link
        return size

    @classmethod
    def from_iterable(cls, iterable):
        head = None

        r = reversed(iterable)
        for e in r:
            link = cls(e, head)
            head = link

        return head


def step1(l, rules):
    head = l
    rest = head.link
    while rest is not None:
        # create and insert new link
        pair = head.value + rest.value
        entry = rules[pair]
        entry = List(entry, rest)
        head.link = entry

        # move to the next pair
        head = rest
        rest = head.link

    return l


def part1(polymer, rules):
    # apply the rules
    l = List.from_iterable(polymer)
    for _ in range(10):
        l = step1(l, rules)

    # count the freqs
    c = Counter(str(l))
    cc = c.most_common()
    most, least = cc[0], cc[-1]
    most, least = most[1], least[1]
    return most - least


def part2(polymer, rules):
    # build out initial state counts
    states = {rule: 0 for rule in rules}
    for pair in sliding_window(polymer, 2):
        p = ''.join(pair)
        states[p] += 1

    # build out transitions map
    transitions = {}
    for a, b in rules.items():
        transitions[a] = (a[0] + b, b + a[1])

    # track counts during the sim
    c = Counter(polymer)

    # apply state transitions for each step
    for i in range(40):
        next = states.copy()
        for pair, count in states.items():
            ts = transitions[pair]
            c[ts[0][1]] += count

            next[pair] -= count
            for t in ts:
                next[t] += count

        states = next

    cc = c.most_common()
    most, least = cc[0], cc[-1]
    most, least = most[1], least[1]
    return most - least


if __name__ == '__main__':
    polymer = None
    rules = {}
    for line in fileinput.input():
        line = line.strip()
        if len(line) == 0:
            continue

        if polymer is None:
            polymer = line
            continue

        rule = line.split()
        rules[rule[0]] = rule[2]

    print(part1(polymer, rules))
    print(part2(polymer, rules))
