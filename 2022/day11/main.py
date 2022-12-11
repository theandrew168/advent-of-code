from collections import namedtuple
import fileinput
import math

from more_itertools import split_at


Op = namedtuple('Op', 'a op b')
Test = namedtuple('Test', 'divisible true false')


class Monkey:

    def __init__(self, items, op, test):
        self.inspections = 0
        self.items = items
        self.op = op
        self.test = test

    def __str__(self):
        return '\n'.join(map(str, [self.items, self.op, self.test]))


def parse(lines):
    monkeys = []
    for info in split_at(lines, lambda x: x == ''):
        _, items, op, divisible, true, false = info

        items = items.split(':')[1].strip()
        items = items.split(',')
        items = [int(item.strip()) for item in items]

        op = op.split('=')[1].strip()
        op = Op(*op.split())

        divisible = int(divisible.split()[-1])
        true = int(true.split()[-1])
        false = int(false.split()[-1])
        test = Test(divisible, true, false)

        monkey = Monkey(items, op, test)
        monkeys.append(monkey)

    return monkeys


def worry(item, op):
    a = item if op.a == 'old' else int(op.a)
    b = item if op.b == 'old' else int(op.b)
    if op.op == '+':
        return a + b
    elif op.op == '*':
        return a * b


def check(item, test):
    if item % test.divisible == 0:
        return test.true
    else:
        return test.false


def part1(lines):
    monkeys = parse(lines)
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.pop(0)
                monkey.inspections += 1
                new_item = worry(item, monkey.op)
                new_item //= 3
                throw = check(new_item, monkey.test)
                monkeys[throw].items.append(new_item)

    counts = [monkey.inspections for monkey in monkeys]
    counts.sort(reverse=True)
    return math.prod(counts[:2])


def part2(lines):
    monkeys = parse(lines)
    divs = [m.test.divisible for m in monkeys]
    lcm = math.lcm(*divs)
    print(lcm)
    for r in range(10000):
        print(f'round {r}')
        for monkey in monkeys:
            while monkey.items:
                item = monkey.items.pop(0)
                monkey.inspections += 1
                new_item = worry(item, monkey.op)
                if new_item >= lcm:
                    new_item //= lcm 
                throw = check(new_item, monkey.test)
                monkeys[throw].items.append(new_item)

    counts = [monkey.inspections for monkey in monkeys]
    counts.sort(reverse=True)
    return math.prod(counts[:2])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
