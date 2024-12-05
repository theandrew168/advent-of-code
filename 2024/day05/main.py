from collections import defaultdict
import fileinput
import functools


def parse(lines):
    rules = defaultdict(set)
    updates = []

    mode = 'rules'
    for line in lines:
        if not line:
            mode = 'updates'
            continue
        if mode == 'rules':
            a, b = line.split('|')
            a, b = int(a), int(b)
            rules[a].add(b)
        if mode == 'updates':
            updates.append([int(n) for n in line.split(',')])
    return rules, updates


def part1(lines):
    rules, updates = parse(lines)

    correct = []
    for update in updates:
        valid = True
        # for each page, lookup it's "comes before" rules
        for i, page in enumerate(update):
            rs = rules[page]
            for r in rs:
                # if the rule isn't in this update, ignore
                if r not in update:
                    continue
                # otherwise check if the "comes before" rule is violated
                ifound = update.index(r)
                if ifound < i:
                    valid = False

        if valid:
            correct.append(update)

    total = 0
    for c in correct:
        total += c[len(c) // 2]
    return total


def part2(lines):
    rules, updates = parse(lines)

    incorrect = []
    for update in updates:
        valid = True
        for i, page in enumerate(update):
            rs = rules[page]
            for r in rs:
                if r not in update:
                    continue
                ifound = update.index(r)
                if ifound < i:
                    valid = False

        if not valid:
            incorrect.append(update)

    # comparison-style sort func based on "comes before" rules
    def before(a, b):
        rs = rules[a]
        if b in rs:
            return -1
        return 0

    # sort each incorrect update based on rule ordering
    correct = []
    for ic in incorrect:
        fixed = sorted(ic, key=functools.cmp_to_key(before))
        correct.append(fixed)

    total = 0
    for c in correct:
        total += c[len(c) // 2]
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
