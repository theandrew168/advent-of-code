from collections import namedtuple
import fileinput

Literal = namedtuple('Literal', 'version type value bits')
OpLength = namedtuple('OpLength', 'version type id length bits')
OpNumber = namedtuple('OpNumber', 'version type id number bits')


class Packet:

    def __init__(self, version, type):
        self.version = version
        self.type = type

        self.value = None
        self.children = []


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
            p = Literal(v, t, value, pbits)
            yield p

        # operator (recursion)
        else:
            pbits += bits[0]
            i, bits = bits[0], bits[1:]
            i = int(i, base=2)

            if i == 0:
                pbits += bits[:15]
                l, bits = bits[:15], bits[15:]
                l = int(l, base=2)

                yield OpLength(v, t, i, l, pbits)
                yield from decode(bits[:l])
                bits = bits[l:]
            else:
                pbits += bits[:11]
                n, bits = bits[:11], bits[11:]
                n = int(n, base=2)

                yield OpNumber(v, t, i, n, pbits)

                size = 0
                for i, s in enumerate(decode(bits)):
                    if i >= n:
                        break
                    size += len(s.bits)
                    yield s

                bits = bits[size:]


def part1(bits):
    return sum(p.version for p in decode(bits))


def pcount(p, ps):
    if isinstance(p, OpNumber):
        return p.number

    count = 0
    size = 0
    while size < p.length:
        size += len(ps[count]).bits
        count += 1

    return count


def treeify(ps):
    head, tail = ps[0], ps[1:]
    if head.type == 4:
        return head.value
    else:
        return list(treeify(tail))


def peval(ps):
    head, tail = ps[0], ps[1:]
    if head.type == 4:
        return head.value

    count = pcount(head, tail)
    ps = tail[:count]

    print(count, ps)
#    if head.type == 0:
#        res = 0
#        for p in ps:
#            res += peval(p


def part2(bits):
    ps = list(decode(bits))
    print(treeify(ps))
    return peval(ps)


if __name__ == '__main__':
    t = None
    for line in fileinput.input():
        t = line.strip()

    # convert hex pairs to binary
    bits = ''
    for h in t:
        n = int(h, base=16)
        bits += '{:04b}'.format(n)

    for p in decode(bits):
        print(p)

    print(part1(bits))
    print(part2(bits))
