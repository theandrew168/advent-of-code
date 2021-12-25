import fileinput

class Seafloor:

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def __str__(self):
        s = ''
        for y in range(self.height):
            start = y * self.width
            end = start + self.width
            row = self.data[start:end]
            row = ''.join(row)
            s += row + '\n'
        return s

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y

    def copy(self):
        return Seafloor(self.data.copy(), self.width, self.height)

    def index(self, x, y):
        return y * self.width + x

    def get(self, x, y):
        idx = self.index(x, y)
        return self.data[idx]

    def set(self, x, y, v):
        idx = self.index(x, y)
        self.data[idx] = v

    def down(self, x, y):
        return x, (y + 1) % self.height

    def right(self, x, y):
        return (x + 1) % self.width, y

    def step(self):
        changed = 0

        # move right
        new1 = self.copy()
        for x, y in self:
            if self.get(x, y) == '>':
                xx, yy = self.right(x, y)
                if self.get(xx, yy) == '.':
                    new1.set(x, y, '.')
                    new1.set(xx, yy, '>')
                    changed += 1

        # move down
        new2 = new1.copy()
        for x, y in new1:
            if new1.get(x, y) == 'v':
                xx, yy = new1.down(x, y)
                if new1.get(xx, yy) == '.':
                    new2.set(x, y, '.')
                    new2.set(xx, yy, 'v')
                    changed += 1

        self.data = new2.data
        return changed > 0


def part1(seafloor):
    print(seafloor)
    
    count = 0
    while True:
        count += 1
        if not seafloor.step():
            break
        print(count)
        print(seafloor)

    return count


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    data = list(''.join(line for line in lines))
    width = len(lines[0])
    height = len(lines)

    seafloor = Seafloor(data, width, height)
    print(part1(seafloor))
