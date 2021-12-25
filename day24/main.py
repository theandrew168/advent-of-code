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

# if z % 26 + v2 != input:
#   z = z // v1 (1 or 26)
#   z = z * 26
#   z = z + input + v3
# else:
#   z = z // v1

# if z & 1 + v2 != input:
#   z = z >> v1 (0 or 1)
#   z = z << 1
#   z = z + input + v3
# else:
#   z = z >> v1 (0 or 1)

# if last bit of z + v2 equal input:
#   if v1, pop a bit
# else:
#   if v1, pop a bit
#   push a bit
#   z equal z plus input plus v3

# if v1 == 0:
#   if z.last + v2 != input:
#       push a bit
# elif v1 == 1:
#   if z.last + v2 != input:
#       pop a bit
#       push a bit
#   else:
#       pop a bit

# if v1 == 0:
#   push a bit
# elif v1 == 1:
#   if z.last + v2 != input:
#       pop a bit
#       push a bit
#   else:
#       pop a bit

# if v1 == 0:
#   push a bit (input + v3)
# elif v1 == 1:
#   pop a bit
#   if z.last + v2 != input:
#       push a bit (input + v3)

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

    vars = []
    for prog in progs:
        v1 = int(prog[4].split()[-1])
        v2 = int(prog[5].split()[-1])
        v3 = int(prog[15].split()[-1])
        vars.append((v1, v2, v3))

    return 42


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
