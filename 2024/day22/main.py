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
        prev = int(str(s)[-1])
        costs = {}
        changes = []
        for i in range(N):
            s = calc(s)
            price = int(str(s)[-1])
            diff = price - prev
            changes.append(diff)
            prev = price
            if len(changes) < 4:
                continue
            seq = tuple(changes[-4:])
            if seq in costs:
                continue
            costs[seq] = price
        all_costs.append(costs)

    all_seqs = set(seq for seq in costs for costs in all_costs)
    assert all(len(seq) == 4 for seq in all_seqs)
    print(len(all_seqs), 'seqs')

    best = None
    for seq in all_seqs:
        #print(seq)
        total = 0
        for costs in all_costs:
            if seq not in costs:
                continue
            total += costs[seq]
        if best is None or total > best:
            print('best', total, seq)
            best = total
    return best


# 1780 too low
if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
