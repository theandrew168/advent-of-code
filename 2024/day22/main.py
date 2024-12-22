from collections import defaultdict
import fileinput
import functools


@functools.cache
def calc(n):
    s = n
    s = (s ^ (s * 64)) % 16777216
    s = (s ^ (s // 32)) % 16777216
    s = (s ^ (s * 2048)) % 16777216
    return s


def part1(lines):
    total = 0
    for line in lines:
        s = int(line)
        for _ in range(2000):
            s = calc(s)
        total += s
    return total


def part2(lines):
    N = 2000

    all_costs = []
    for line in lines:
        s = int(line)
        prev = s % 10
        costs = {}
        changes = []
        for i in range(N):
            s = calc(s)
            price = s % 10
            diff = price - prev
            changes.append(diff)
            prev = price
            if len(changes) < 4:
                continue
            seq = tuple(changes[-4:])
            if seq in costs:
                continue
            costs[seq] = price
        assert len(changes) == N
        all_costs.append(costs)

    all_seqs = set()
    for costs in all_costs:
        for seq in costs:
            all_seqs.add(seq)
    assert all(len(seq) == 4 for seq in all_seqs)

    scores = defaultdict(int)
    for seq in all_seqs:
        total = 0
        for costs in all_costs:
            if seq not in costs:
                continue
            total += costs[seq]
        scores[seq] = total

    return max(scores.values())


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
