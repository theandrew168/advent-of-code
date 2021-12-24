import fileinput


class Inst:

    def __init__(self, name, dst, src):
        self.name = name
        self.dst = dst
        self.src = src

    def __str__(self):
        s = '({!s} {!s} {!s})'
        return s.format(self.name, self.dst, self.src)

    def __repr__(self):
        s = 'Inst({!r}, {!r}, {!r})'
        return s.format(self.name, self.dst, self.src)


# build an AST and do some analysis
def part1(lines):
    inputs = sum(1 for line in lines if 'inp' in line)

    regs = [None] * 4
    for line in reversed(lines):
        name, dst, *src = line.split()
        if len(src) == 1:
            src = src[0]
        else:
            # will be an inp inst here
            inputs -= 1
            src = 'input_{}'.format(inputs)

        inst = Inst(name, dst, src)
        print(inst)

        # build a graph of instructions
        idx = 'wxyz'.index(dst)
        inst.dst = regs[idx]
        if inst.src in 'wxyz':
            idx2 = 'wxyz'.index(inst.src)
            inst.src = regs[idx2]
        regs[idx] = inst

    print(repr(regs[3]))
#    for r in regs:
#        print(repr(r))

    return 42


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
