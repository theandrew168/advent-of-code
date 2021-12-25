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


def part1(lines):
    progs = []
    for line in lines:
        if line.startswith('inp'):
            progs.append([line])
        else:
            progs[-1].append(line)

    want = [set([0])]
    for prog in reversed(progs):
        print('solving', len(want) - 1)

        outputs = set()
        for z in range(100000):
            for c in range(1, 10):
                alu = ALU(c)
                alu.z = z
                for inst in prog:
                    alu.execute(inst)

                if alu.z in want[-1]:
                    outputs.add(z)
                    break

        if not outputs:
            raise ValueError('no outputs')

        want.append(outputs)

    code = []
    want = list(reversed(want))
    for i, prog in enumerate(prog):
        print('coding', len(code))
        for z in want[i]:
            for c in range(9, 0, -1):
                alu = ALU(c)
                alu.z = z
                for inst in prog:
                    alu.execute(prog)

                if alu.z in want[i]:
                    code.append(c)
                    break

    return ''.join(str(c) for c in code)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
