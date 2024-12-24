from collections import deque
import fileinput


def parse(lines):
    wires = {}
    gates = []
    for line in lines:
        if ':' in line:
            k, v = line.split(': ')
            wires[k] = bool(int(v))
        elif '->' in line:
            gate = line.split()
            gate = tuple([gate[0], gate[1], gate[2], gate[4]])
            gates.append(gate)
    return wires, gates


def part1(lines):
    wires, gates = parse(lines)
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

    zs = [wire for wire in wires if wire[0] == 'z']
    zs = sorted(zs, reverse=True)
    bits = [int(wires[z]) for z in zs]
    bits = ''.join(str(bit) for bit in bits)
    return int(bits, base=2)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
