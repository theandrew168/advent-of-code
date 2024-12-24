from collections import defaultdict, deque
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
    tries = 0
    wires = dict(wires)
    gates = deque(gates)
    while gates:
        tries += 1
        if tries >= 10000:
            return {}
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


def find_gate(gates, a=None, op=None, b=None, c=None):
    preds = []
    if a is not None:
        preds.append(lambda g: g[0] == a or g[2] == a)
    if op is not None:
        preds.append(lambda g: g[1] == op)
    if b is not None:
        preds.append(lambda g: g[2] == b or g[0] == b)
    if c is not None:
        preds.append(lambda g: g[3] == c)

    for gate in gates:
        if all(pred(gate) for pred in preds):
            return gate


def swap(gates, a, b):
    gg = set(gates)
    aa = (a[0], a[1], a[2], b[3])
    bb = (b[0], b[1], b[2], a[3])
    gg.remove(a)
    gg.remove(b)
    gg.add(aa)
    gg.add(bb)
    return gg


def graphviz(gates):
    print('digraph G {')
    for gate in gates:
        shape = 'box'
        if gate[1] == 'XOR':
            shape = 'doublecircle'
        elif gate[1] == 'OR':
            shape = 'circle'
        elif gate[1] == 'AND':
            shape = 'diamond'

        print('{} [label="{}", shape="{}"]'.format(gate[3], gate[1] + ' ' + gate[3], shape))
        print('{} -> {}'.format(gate[0], gate[3]))
        print('{} -> {}'.format(gate[2], gate[3]))
    print('}')


# Half Adder:
# https://circuitdigest.com/sites/default/files/projectimage_tut/Half-Adder-Circuit-and-Its-Construction.png
#
# Full Adder:
# https://circuitdigest.com/sites/default/files/projectimage_tut/Full-Adder-Circuit.png
#
# Assumptions:
# 1. Every xN and yN input must lead into a XOR
# 2. Every xN and yN input must lead into an AND
# 3. Every zN output must come from a XOR
def part2(lines):
    wires, gates = parse(lines)
    #graphviz(gates)
    #return

    # solved via manual inspection of the circuit graph
    swaps = [
        # 16
        'z16', 'hmk',
        # 20
        'z20', 'fhp',
        # 27
        'rvf', 'tpc',
        # 33
        'z33', 'fcd',
    ]

    return ','.join(sorted(swaps))

    # x00, y00, and z00 are a half adder
    # all others are full adders
    all_swapped = set()
    for i in range(45):
        x = 'x{:02d}'.format(i)
        y = 'y{:02d}'.format(i)
        z = 'z{:02d}'.format(i)

        # x XOR y -> mid (not z)
        in_xor = find_gate(gates, a=x, op='XOR', b=y)
        if in_xor[3][0] == 'z':
            all_swapped.add(in_xor)

        # x AND y -> out_or (not z)
        in_and = find_gate(gates, a=x, op='AND', b=y)
        if in_and[3][0] == 'z':
            all_swapped.add(in_and)

        # mid XOR carry -> z
        out_xor = find_gate(gates, a=in_xor[3], op='XOR', c=z)
        if not out_xor:
            # the swapped gate will have an output of z
            swapped = find_gate(gates, c=z)
            assert swapped is not None
            all_swapped.add(swapped)

        mid = find_gate(gates, a=in_xor[3], op='AND')
        if not mid:
            # if mid can't be found, in_xor's output must be wrong
            all_swapped.add(in_xor)

        # in_and OR mid -> carry
        out_or = find_gate(gates, a=in_and[3], op='OR')
        if not out_or:
            # if out_or can't be found, in_and's output must be wrong
            all_swapped.add(in_and)

        print('Adder {}'.format(i))
        print('in_xor', in_xor)
        print('in_and', in_and)
        print('mid', mid)
        print('out_xor', out_xor)
        print('out_or', out_or)
        print()

    import pprint
    pprint.pprint(all_swapped)

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

    for gs in itertools.permutations(all_swapped):
        p00, p01, p10, p11, p20, p21, p30, p31 = gs
        maybe_gates = swap(gates, p00, p01)
        maybe_gates = swap(maybe_gates, p10, p11)
        maybe_gates = swap(maybe_gates, p20, p21)
        maybe_gates = swap(maybe_gates, p30, p31)
        maybe_wires = solve(wires, maybe_gates)
        if not maybe_wires:
            continue

        zs = [wire for wire in maybe_wires if wire[0] == 'z']
        zs = sorted(zs, reverse=True)
        zs = [int(maybe_wires[z]) for z in zs]
        z = ''.join(str(bit) for bit in zs)
        z = int(z, base=2)
        if z == x + y:
            return gs


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
