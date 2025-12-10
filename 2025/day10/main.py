from collections import Counter, deque
import fileinput
import functools
import itertools
from pprint import pprint
from queue import PriorityQueue

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def parse(line):
    lights, *buttons, joltage = line.split()
    lights = lights[1:-1]
    buttons = [
        set(int(n) for n in button[1:-1].split(',')) for button in buttons
    ]
    joltage = tuple(int(n) for n in joltage[1:-1].split(','))
    return lights, buttons, joltage


def press1(lights, button):
    s = ''
    for i, c in enumerate(lights):
        if i in button:
            if c == '.':
                s += '#'
            else:
                s += '.'
        else:
            s += c
    return s


def solve1(dest, buttons):
    start = '.' * len(dest)

    costs = {}
    costs[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, lights = pq.get()
        for button in buttons:
            new_cost = cost + 1
            new_lights = press1(lights, button)
            if new_lights == dest:
                return new_cost
            if new_lights not in costs or new_cost < costs[new_lights]:
                costs[new_lights] = new_cost
                pq.put((new_cost, new_lights))


def press2(jolts, button):
    new_jolts = []
    for i, j in enumerate(jolts):
        if i in button:
            new_jolts.append(j+1)
        else:
            new_jolts.append(j)
    return tuple(new_jolts)


def dist(dest, jolts):
    dist = 0
    for i in range(len(dest)):
        diff = dest[i] - jolts[i]
        if diff < 0:
            return 999999999999
        dist += diff
    return dist


def solve2(dest, buttons):
    start = tuple([0] * len(dest))

    costs = {}
    costs[start] = 0

    pq = PriorityQueue()
    pq.put((0, 0, start))
    while not pq.empty():
        steps, cost, jolts = pq.get()
        for button in buttons:
            new_jolts = press2(jolts, button)
            d = dist(dest, new_jolts)
            new_cost = cost + 1 + d
            new_steps = steps + 1
            print(new_steps, new_cost, new_jolts, dest)
            input()
            if new_jolts == dest:
                return new_steps
            if new_jolts not in costs or new_cost < costs[new_jolts]:
                costs[new_jolts] = new_cost
                pq.put((new_steps, new_cost, new_jolts))


def part1(lines):
    total = 0
    for line in lines:
        l, b, j = parse(line)
        total += solve1(l, b)
    return total


def part2(lines):
    total = 0
    for line in lines:
        l, b, j = parse(line)
        score = solve2(j, b)
        print(score)
        total += score
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
