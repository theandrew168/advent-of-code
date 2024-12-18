from collections import defaultdict
import fileinput

# Register A: 64751475
# Register B: 0
# Register C: 0
# 
# Program: 2,4, 1,2, 7,5, 4,5, 1,3, 5,5, 0,3, 3,0

# 2 4 (bst)
# B = A % 8
#
# 1 2 (bxl)
# B = B ^ 2 (0b010)
#
# 7 5 (cdv)
# C = A // 2**B
#
# 4 5 (bxc)
# B = B ^ C
#
# 1 3 (bxl)
# B = B ^ 3 (0b011)
# 
# 5 5 (out)
# OUT += B % 8
#
# 0 3 (adv)
# A = A // 2**3 (8)
#
# 3 0 (jnz)
# IF A != 0: GOTO 0

# The program:
#
# B = A % 8
# B = B ^ 2 (0b010)
# C = A // 2**B
# B = B ^ C
# B = B ^ 3 (0b011)
# OUT += B % 8
# A = A // 8
# IF A == 0: DONE!
#
# Terminates when A == 0.

# To output the last number: 0
# A = 0
# A < 8 (to div out to zero)
# B (bottom 3) must be 0b000 (0)
# B (buttom 3) must be 0b011 (3)
# B ^ C = 0b011 (3)
# C = A // (2**B)
# B = B ^ 2
# B = A % 8

# B ^ C = 0b011 (3)
# (A%8)^2 ^ (A // 2**(A%8)^2) = 0b011 (3)
# C = A // (2**(A % 8)^2)
# B = (A % 8) ^ 2

#A = 0
#PROG = [2,4, 1,2, 7,5, 4,5, 1,3, 5,5, 0,3, 3,0]
#for p in reversed(PROG):
#    O = p
#    B = O
#    B = B ^ 3


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

    # iteratively build up the program from end to start
    A = 0
    for i in range(len(prog)):
        # we want to create the following output (building from the end)
        want = prog[-(i+1):]
        while True:
            # run the output for the current A
            out = run([A, regs[1], regs[2]], prog)
            # if it gives us the correct result, shift left by 3 and keep rolling
            if out == want:
                A <<= 3
                break
            # if it doesn't give us the output we want, keep looping
            A += 1
    # final answer was shifted an extra time to undo it before returning
    return A >> 3


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
