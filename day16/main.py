from collections import namedtuple
import fileinput

Literal = namedtuple('Literal', 'version type value bits')
OpLength = namedtuple('OpLength', 'version type id length bits')
OpNumber = namedtuple('OpNumber', 'version type id number bits')


class Packet:

    def __init__(self, version, type, bits, *, value=None, id=None, children=None):
        self.version = version
        self.type = type
        self.bits = bits

        self.value = value
        self.id = id
        self.children = children or []

    def pprint(self, depth=0):
        pad = ' ' * depth
        print(pad + str(self))
        for c in self.children:
            c.pprint(depth + 1)

    def __str__(self):
        s = '{} {} '.format(self.version, self.type)
        if self.value:
            s += str(self.value) + ' '
        else:
            s += str(self.id) + ' '
        s += str(self.bits)
        return s


def decode(bits):
    # parse and yield out each packet
    while '1' in bits:
        pbits = ''

        # version / type
        pbits += bits[:6]
        v, t, bits = bits[:3], bits[3:6], bits[6:] 
        v, t = int(v, base=2), int(t, base=2)

        # literal
        if t == 4:
            value = ''
            while True:
                pbits += bits[:5]
                g, bits = bits[:5], bits[5:]
                value += g[1:]
                if g[0] == '0':
                    break

            value = int(value, base=2)
            packet = Packet(v, t, pbits, value=value)
            return packet

        # operator (recursion)
        else:
            pbits += bits[0]
            i, bits = bits[0], bits[1:]
            i = int(i, base=2)

            if i == 0:
                pbits += bits[:15]
                l, bits = bits[:15], bits[15:]
                l = int(l, base=2)

                size = 0
                children = []
                while size < l:
                    c = decode(bits[size:l])
                    children.append(c)
                    size += len(c.bits)
                    pbits += c.bits

                bits = bits[l:]
                return Packet(v, t, pbits, id=i, children=children)
            else:
                pbits += bits[:11]
                n, bits = bits[:11], bits[11:]
                n = int(n, base=2)

                size = 0
                count = 0
                children = []
                while count < n:
                    c = decode(bits[size:])
                    children.append(c)
                    size += len(c.bits)
                    pbits += c.bits
                    count += 1

                bits = bits[size:]
                packet = Packet(v, t, pbits, id=i, children=children)
                return packet


def score1(p):
    res = p.version
    for c in p.children:
        res += score1(c)
    return res


def part1(p):
    return score1(p)


def score2(p):
    if p.type == 0:
        res = 0
        for c in p.children:
            res += score2(c)
        return res

    if p.type == 1:
        res = 1
        for c in p.children:
            res *= score2(c)
        return res

    if p.type == 2:
        res = []
        for c in p.children:
            res.append(score2(c))
        return min(res)

    if p.type == 3:
        res = []
        for c in p.children:
            res.append(score2(c))
        return max(res)

    if p.type == 4:
        return p.value

    if p.type == 5:
        res = []
        for c in p.children:
            res.append(score2(c))
        return res[0] > res[1]

    if p.type == 6:
        res = []
        for c in p.children:
            res.append(score2(c))
        return res[0] < res[1]

    if p.type == 7:
        res = []
        for c in p.children:
            res.append(score2(c))
        return res[0] == res[1]


def part2(p):
    return score2(p)


if __name__ == '__main__':
    t = None
    for line in fileinput.input():
        t = line.strip()

    # convert hex pairs to binary
    bits = ''
    for h in t:
        n = int(h, base=16)
        bits += '{:04b}'.format(n)

    p = decode(bits)
    print(part1(p))
    print(part2(p))
