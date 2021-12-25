import fileinput


class ALU:

    def __init__(self, data):
        self.data = data
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        s = 'w={} x={} y={} z={}'
        return s.format(self.w, self.x, self.y, self.z)

    def value(self, v):
        try:
            v = int(v)
        except ValueError:
            v = getattr(self, v)
        return v

    def execute(self, line):
        inst, *args = line.split()
        if len(args) == 2:
            a, b = args
        else:
            a = args[0]
            b = self.data

        if inst == 'inp':
            setattr(self, a, int(b))
        elif inst == 'add':
            setattr(self, a, getattr(self, a) + self.value(b))
        elif inst == 'mul':
            setattr(self, a, getattr(self, a) * self.value(b))
        elif inst == 'div':
            setattr(self, a, getattr(self, a) // self.value(b))
        elif inst == 'mod':
            setattr(self, a, getattr(self, a) % self.value(b))
        elif inst == 'eql':
            setattr(self, a, 1 if getattr(self, a) == self.value(b) else 0)
        else:
            raise ValueError('invalid instruction: {}'.format(inst))


# x = !(z % 26 + v2 == input)
# z = (z / v1)      (1 or 26)
# y = 25 * x + 1
# z = z * y
# y = (input + v3) * x
# z = z + y
#
# x = z % 26 + v2 != input
# z = z // v1
# z = z * (25 * x + 1)
# z = z + ((input + v3) * x)
# ret z
def sim(i, z, v1, v2, v3):
    x = z % 26 + v2 != i
    z = z // v1
    z = z * (25 * x + 1)
    z = z + ((i + v3) * x)
    return z


def part1(lines):
    progs = []
    for line in lines:
        if line.startswith('inp'):
            progs.append([line])
        else:
            progs[-1].append(line)

    # (1, 10, 1)     push
    # (1, 11, 9)     push
    # (1, 14, 12)    push
    # (1, 13, 6)     push
    # (26, -6, 9)    pop
    # (26, -14, 15)  pop
    # (1, 14, 7)     push
    # (1, 13, 12)    push
    # (26, -8, 15)   pop
    # (26, -15, 3)   pop
    # (1, 10, 6)     push
    # (26, -11, 2)   pop
    # (26, -13, 10)  pop
    # (26, -4, 12)   pop

    params = []
    for prog in progs:
        v1 = int(prog[4].split()[-1])
        v2 = int(prog[5].split()[-1])
        v3 = int(prog[15].split()[-1])
        params.append((v1, v2, v3))

    want = [set([0])]
    for v1, v2, v3 in reversed(params):
        print('solving', len(want) - 1, ' - ', v1, v2, v3)

        outputs = set()
        for i in range(1, 10):
            for z in range(-10**6, 10**6):
                if sim(i, z, v1, v2, v3) in want[-1]:
                    print(i, z)
                    outputs.add(z)
                    break

        print(outputs)
        if not outputs:
            raise ValueError('no outputs')

        want.append(outputs)

    for w in reversed(want):
        print(w)

    return 42
#    code = []
#    want = list(reversed(want))
#    for i, prog in enumerate(prog):
#        print('coding', len(code))
#        for z in want[i]:
#            for c in range(9, 0, -1):
#                alu = ALU(c)
#                alu.z = z
#                for inst in prog:
#                    alu.execute(prog)
#
#                if alu.z in want[i]:
#                    code.append(c)
#                    break
#
#    return ''.join(str(c) for c in code)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
