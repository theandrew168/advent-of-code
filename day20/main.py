import fileinput


class Image:

    def __init__(self, pixels, width, height, padding=55):
        self.width = width + padding + padding
        self.height = height + padding + padding

        self.data = ['.'] * self.width * self.height
        for y in range(height):
            for x in range(width):
                small_idx = y * width + x
                large_idx = (y + padding) * self.width + (x + padding)
                self.data[large_idx] = pixels[small_idx]

    def __str__(self):
        s = ''
        for y in range(self.height):
            start = y * self.width
            end = start + self.width
            s += ''.join(self.data[start:end]) + '\n'
        return s

    def get(self, x, y):
        idx = y * self.width + x
        return self.data[idx]

    def adj9(self, x, y):
        adj = []

        for yoff in [-1, 0, 1]:
            yy = y + yoff
            for xoff in [-1, 0, 1]:
                xx = x + xoff

                if yy < 0 or yy >= self.height:
                    adj.append(self.get(x, y))
                    continue

                if xx < 0 or xx >= self.width:
                    adj.append(self.get(x, y))
                    continue

                adj.append(self.get(xx, yy))

        return adj

    def adj_to_val(self, adj):
        bits = ''
        for pixel in adj:
            if pixel == '.':
                bits += '0'
            else:
                bits += '1'

        bits = ''.join(bits)
        return int(bits, base=2)

    def enhance(self, alg):
        data = []
        for y in range(self.height):
            for x in range(self.width):
                adj = self.adj9(x, y)
                val = self.adj_to_val(adj)
                new = alg[val]
                data.append(new)

        self.data = data

    def lit(self):
        return sum(1 for p in self.data if p == '#')


def part1(image, alg):
    image.enhance(alg)
    image.enhance(alg)
    return image.lit()


def part2(image, alg):
    for _ in range(50):
        image.enhance(alg)
    return image.lit()


if __name__ == '__main__':
    alg = None

    pixels = []
    width = 0
    height = 0
    for line in fileinput.input():
        line = line.strip()
        if alg is None:
            alg = line
            continue

        if len(line) == 0:
            continue

        width = len(line)
        height += 1
        pixels.extend(line)

    print(part1(Image(pixels, width, height), alg))
    print(part2(Image(pixels, width, height), alg))
