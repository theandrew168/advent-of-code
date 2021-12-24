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
            b = self.data[0]
            self.data = self.data[1:]

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


# cant brute force this
# need to trace the formula back and then SAT solve?
# maybe use pycosat or something
# like that one minecraft redstone CTF from LiveOverflow
def part1(lines):
    code = 99999999999999
    while True:
        print(code)
        alu = ALU(str(code))
        for line in lines:
            alu.execute(line)

        if alu.z == 0:
            break

        code -= 1

    return code


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
