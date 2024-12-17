import fileinput


def parse(lines):
    a = int(lines[0].split()[-1])
    b = int(lines[1].split()[-1])
    c = int(lines[2].split()[-1])
    prog = lines[4].split()[1]
    prog = [int(n) for n in prog.split(',')]
    return [a, b, c], prog


def run(regs, prog):
    out = []

    pc = 0
    while pc < len(prog):
        inst = prog[pc]

        # adv
        if inst == 0:
            op = prog[pc+1]
            op = op if op <= 3 else regs[op-4]
            regs[0] = regs[0] // 2**op
            pc += 2
        # bxl
        elif inst == 1:
            op = prog[pc+1]
            regs[1] = regs[1] ^ op
            pc += 2
        # bst
        elif inst == 2:
            op = prog[pc+1]
            op = op if op <= 3 else regs[op-4]
            regs[1] = op % 8
            pc += 2
        # jnz
        elif inst == 3:
            op = prog[pc+1]
            if regs[0] != 0:
                pc = op
            else:
                pc += 2
        # bxc
        elif inst == 4:
            regs[1] = regs[1] ^ regs[2]
            pc += 2
        # out
        elif inst == 5:
            op = prog[pc+1]
            op = op if op <= 3 else regs[op-4]
            out.append(op % 8)
            pc += 2
        # bdv
        elif inst == 6:
            op = prog[pc+1]
            op = op if op <= 3 else regs[op-4]
            regs[1] = regs[0] // 2**op
            pc += 2
        # cdv
        elif inst == 7:
            op = prog[pc+1]
            op = op if op <= 3 else regs[op-4]
            regs[2] = regs[0] // 2**op
            pc += 2

    return out


def part1(lines):
    regs, prog = parse(lines)
    out = run(regs, prog)
    return ','.join(str(n) for n in out)


def part2(lines):
    regs, prog = parse(lines)

    i = 0
    while True:
        out = run([i, regs[1], regs[2]], prog)
        if out == prog:
            break
    return i


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
