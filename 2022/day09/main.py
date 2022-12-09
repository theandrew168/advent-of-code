from collections import namedtuple
import fileinput


Point = namedtuple('Point', 'x y')


def nearby(a, b):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            c = Point(a.x + dx, a.y + dy)
            if c == b:
                return True

    return False


class Rope:

    def __init__(self, knots=2):
        self.knots = [Point(0, 0)] * knots

    def move(self, direction):
        if direction == 'U':
            self.up(0)
        elif direction == 'D':
            self.down(0)
        elif direction == 'L':
            self.left(0)
        elif direction == 'R':
            self.right(0)

    def up(self, idx):
        self.knots[idx] = Point(self.knots[idx].x, self.knots[idx].y + 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x == head.x:
            self.up(idx + 1)
        elif tail.x < head.x:
            self.up_right(idx + 1)
        elif tail.x > head.x:
            self.up_left(idx + 1)

    def down(self, idx):
        self.knots[idx] = Point(self.knots[idx].x, self.knots[idx].y - 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x == head.x:
            self.down(idx + 1)
        elif tail.x < head.x:
            self.down_right(idx + 1)
        elif tail.x > head.x:
            self.down_left(idx + 1)

    def left(self, idx):
        self.knots[idx] = Point(self.knots[idx].x - 1, self.knots[idx].y)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.y == head.y:
            self.left(idx + 1)
        elif tail.y < head.y:
            self.up_left(idx + 1)
        elif tail.y > head.y:
            self.down_left(idx + 1)

    def right(self, idx):
        self.knots[idx] = Point(self.knots[idx].x + 1, self.knots[idx].y)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.y == head.y:
            self.right(idx + 1)
        elif tail.y < head.y:
            self.up_right(idx + 1)
        elif tail.y > head.y:
            self.down_right(idx + 1)

    def up_left(self, idx):
        self.knots[idx] = Point(self.knots[idx].x - 1, self.knots[idx].y + 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x != head.x and tail.y != head.y:
            self.up_left(idx + 1)
        elif tail.x == head.x:
            self.up(idx + 1)
        elif tail.y == head.y:
            self.left(idx + 1)

    def up_right(self, idx):
        self.knots[idx] = Point(self.knots[idx].x + 1, self.knots[idx].y + 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x != head.x and tail.y != head.y:
            self.up_right(idx + 1)
        elif tail.x == head.x:
            self.up(idx + 1)
        elif tail.y == head.y:
            self.right(idx + 1)

    def down_left(self, idx):
        self.knots[idx] = Point(self.knots[idx].x - 1, self.knots[idx].y - 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x != head.x and tail.y != head.y:
            self.down_left(idx + 1)
        elif tail.x == head.x:
            self.down(idx + 1)
        elif tail.y == head.y:
            self.left(idx + 1)

    def down_right(self, idx):
        self.knots[idx] = Point(self.knots[idx].x + 1, self.knots[idx].y - 1)
        if idx + 1 == len(self.knots):
            return

        head, tail = self.knots[idx], self.knots[idx + 1]
        if nearby(head, tail):
            return

        if tail.x != head.x and tail.y != head.y:
            self.down_right(idx + 1)
        elif tail.x == head.x:
            self.down(idx + 1)
        elif tail.y == head.y:
            self.right(idx + 1)


def parse(lines):
    for line in lines:
        d, s = line.split()
        yield d, int(s)


def part1(lines):
    visited = set()
    rope = Rope()

    moves = parse(lines)
    for direction, steps in parse(lines):
        for _ in range(steps):
            rope.move(direction)
            visited.add(rope.knots[-1])

    return len(visited)


def part2(lines):
    visited = set()
    rope = Rope(knots=10)

    moves = parse(lines)
    for direction, steps in list(parse(lines)):
        for _ in range(steps):
            rope.move(direction)
            visited.add(rope.knots[-1])

    return len(visited)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
