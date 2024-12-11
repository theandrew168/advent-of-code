from collections import defaultdict, deque
import fileinput
import functools


def sim(stone):
    s = str(stone)
    if stone == 0:
        return [1]
    elif len(s)%2 == 0:
        hl = len(s) // 2
        l = s[:hl]
        r = s[hl:]
        return [int(l), int(r)]
    else:
        return [stone * 2024]


def gen(stones):
    new = []
    for stone in stones:
        new.extend(sim(stone))
    return new


def part1(lines):
    stones = [int(s) for s in lines[0].split()]
    for i in range(25):
        stones = gen(stones)
    return len(stones)


"""
We can't sim the whole thing: too large / too slow.
Stones form cycles that can be cached.
For example, 0 after N generations always yields the same result.
Is this a graph / tree? How do I represent values vs refs?
Map initial values to generations as an array?

{
  0: [[0], [1], [2024], [20, 24]],
  1: [[1], [2024], [20, 24]],
  2024: [[2024], [20, 24]],
  20: [[20]],
  24: [[24]],
}

Or a directed cyclic graph:

0 -> 1
1 -> 2024
2024 -> 20
2024 -> 24
20 -> 2
20 -> 0
24 -> 2
24 -> 4

With a graph, solving becomes a recursive counting problem.

Sim from 0:

0 [0]
1 [1]
2 [2024]
3 [20, 24]
4 [2, 0, 2, 4]
5 [4048, 1, 4048, 8096]
6 [40, 48, 2024, 40, 48, 80, 96]
7 [4, 0, 4, 8, 20, 24, 4, 0, 4, 8, 8, 0, 9, 6]
"""
def part2(lines):
    stones = [int(s) for s in lines[0].split()]

    G = defaultdict(list)

    # build the graph
    Q = deque(stones)
    while Q:
        stone = Q.popleft()
        if stone in G:
            continue
        res = sim(stone)
        G[stone] = res
        Q.extend(res)

    # count the stones (memoized)
    @functools.cache
    def count(stone, depth):
        if depth >= 75:
            return 0
        edges = G[stone]
        return len(edges) - 1 + sum(count(s, depth+1) for s in edges)

    return len(stones) + sum(count(stone, 0) for stone in stones)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
