from collections import deque
import fileinput
import itertools


def parse(lines):
    wires = {}
    gates = set()
    for line in lines:
        if ':' in line:
            k, v = line.split(': ')
            wires[k] = bool(int(v))
        elif '->' in line:
            gate = line.split()
            gate = tuple([gate[0], gate[1], gate[2], gate[4]])
            gates.add(gate)
    return wires, gates


def solve(wires, gates):
    wires = dict(wires)
    gates = deque(gates)
    while gates:
        gate = gates.popleft()
        a, op, b, c = gate
        if a not in wires or b not in wires:
            gates.append(gate)
            continue
        if op == 'AND':
            wires[c] = wires[a] & wires[b]
        elif op == 'OR':
            wires[c] = wires[a] | wires[b]
        elif op == 'XOR':
            wires[c] = wires[a] ^ wires[b]
        else:
            assert False
    return wires


def part1(lines):
    wires, gates = parse(lines)
    wires = solve(wires, gates)

    zs = [wire for wire in wires if wire[0] == 'z']
    zs = sorted(zs, reverse=True)
    zs = [int(wires[z]) for z in zs]
    z = ''.join(str(bit) for bit in zs)
    z = int(z, base=2)
    return z


def part2(lines):
    wires, gates = parse(lines)

    xs = [w for w in wires if w[0] == 'x']
    xs = sorted(xs, reverse=True)
    xs = [int(wires[x]) for x in xs]
    x = ''.join(str(bit) for bit in xs)
    x = int(x, base=2)

    ys = [w for w in wires if w[0] == 'y']
    ys = sorted(ys, reverse=True)
    ys = [int(wires[y]) for y in ys]
    y = ''.join(str(bit) for bit in ys)
    y = int(y, base=2)

    print('{} + {} = {}'.format(x, y, x + y))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
