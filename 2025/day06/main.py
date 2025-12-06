import fileinput
import math

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


# Parse ops and nums while keeping all whitespace intact.
def parse(lines):
    ops = []
    for i, c in enumerate(lines[-1]):
        if c != ' ':
            ops.append((c, i))

    nums = [[] for _ in ops]
    for line in lines[:-1]:
        cur = 0
        for i in range(len(ops)-1):
            c, start = ops[i]
            e, end = ops[i+1]
            nums[i].append(line[start:end - (0 if e == '\n' else 1)])

    ops = [op[0] for op in ops[:-1]]
    return ops, nums


def part1(lines):
    ops, nums = parse(lines)

    total = 0
    for i, op in enumerate(ops):
        if op == '*':
            total += math.prod(int(n) for n in nums[i])
        elif op == '+':
            total += sum(int(n) for n in nums[i])
    return total


def part2(lines):
    ops, nums = parse(lines)

    total = 0
    for i, op in enumerate(ops):
        col = nums[i]
        w = len(col[0])

        ns = []
        for j in range(w-1, -1, -1):
            num = ''
            for w in col:
                num += w[j]
            ns.append(num)

        if op == '*':
            total += math.prod(int(n) for n in ns)
        elif op == '+':
            total += sum(int(n) for n in ns)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
