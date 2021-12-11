from collections import namedtuple
import fileinput


Instruction = namedtuple('Instruction', 'action n')


class Sub1:

    def __init__(self):
        self.position = 0
        self.depth = 0

    def forward(self, n):
        self.position += n

    def down(self, n):
        self.depth += n

    def up(self, n):
        self.depth -= n


class Sub2:

    def __init__(self):
        self.position = 0
        self.depth = 0
        self.aim = 0

    def forward(self, n):
        self.position += n
        self.depth += self.aim * n

    def down(self, n):
        self.aim += n

    def up(self, n):
        self.aim -= n



def part1(instructions):
    sub = Sub1()
    for i in instructions:
        if i.action == 'forward':
            sub.forward(i.n)
        elif i.action == 'down':
            sub.down(i.n)
        elif i.action == 'up':
            sub.up(i.n)

    return sub.position * sub.depth


def part2(instructions):
    sub = Sub2()
    for i in instructions:
        if i.action == 'forward':
            sub.forward(i.n)
        elif i.action == 'down':
            sub.down(i.n)
        elif i.action == 'up':
            sub.up(i.n)

    return sub.position * sub.depth


if __name__ == '__main__':
    instructions = []
    for line in fileinput.input():
        action, n = line.split()
        n = int(n)
        i = Instruction(action, n)
        instructions.append(i)

    print(part1(instructions))
    print(part2(instructions))
