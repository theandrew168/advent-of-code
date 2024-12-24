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
    bits = [int(wires[z]) for z in zs]
    bits = ''.join(str(bit) for bit in bits)
    return int(bits, base=2)


def swap(gates, a, b):
    gg = set(gates)
    aa = (a[0], a[1], a[2], b[3])
    bb = (b[0], b[1], b[2], a[3])
    gg.remove(a)
    gg.remove(b)
    gg.add(aa)
    gg.add(bb)
    return gg


# 45 Xs
# 45 Ys
# 222 gates

# Rough calcs:
# 222 choose 4 (98491965) * 4 choose 2 (6) = 590951790
def part2(lines):
    base_wires, base_gates = parse(lines)

    xs = [w for w in base_wires if w[0] == 'x']
    xs = sorted(xs, reverse=True)
    xs = [int(base_wires[x]) for x in xs]
    x = ''.join(str(bit) for bit in xs)
    x = int(x, base=2)

    ys = [w for w in base_wires if w[0] == 'y']
    ys = sorted(ys, reverse=True)
    ys = [int(base_wires[y]) for y in ys]
    y = ''.join(str(bit) for bit in ys)
    y = int(y, base=2)

    want = x + y
    print('{} + {} = {}'.format(x, y, want))
    
    for gs in itertools.combinations(base_gates, 4):
        for a, b in itertools.combinations(gs, 2):
            os = set(gs)
            os.remove(a)
            os.remove(b)
            oa, ob = os

            gates = swap(base_gates, a, b)
            gates = swap(base_gates, oa, ob)
            wires = solve(base_wires, gates)

            zs = [wire for wire in wires if wire[0] == 'z']
            zs = sorted(zs, reverse=True)
            zs = [int(wires[z]) for z in zs]
            z = ''.join(str(bit) for bit in zs)
            z = int(z, base=2)
            print(z)
            if z == want:
                print('found', a, b)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
