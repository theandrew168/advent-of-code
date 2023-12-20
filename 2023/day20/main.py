from collections import namedtuple
import fileinput
import math
import queue
import re

Pulse = namedtuple('Pulse', 'state dst src')
Node = namedtuple('Node', 'module edges')


def parse(lines):
    graph = {}

    for line in lines:
        toks = re.split('[,\s]+', line)
        k, _, *vals = toks
        if k[0] == '%':
            m = dict(kind='ff', state=False)
            graph[k[1:]] = Node(m, vals)
        elif k[0] == '&':
            ins = []
            for l in lines:
                ts = re.split('[,\s]+', l)
                if k[1:] in ts[2:]:
                    ins.append(ts[0][1:])
            m = dict(kind='conj', state={ i: False for i in ins })
            graph[k[1:]] = Node(m, vals)
        else:
            m = dict(kind='broad')
            graph[k] = Node(m, vals)

    return graph


def sim(graph, cycle=None, highs=None):
    ls = 0
    hs = 0

    q = queue.Queue()
    q.put(Pulse('low', 'broadcaster', 'button'))
    while not q.empty():
        pulse = q.get()
#        print(pulse)
        if pulse.state == 'low':
            ls += 1
        else:
            hs += 1

        # rx's parents, found via manual input analysis
        want = ['xc', 'th', 'pd', 'bp']
        if cycle is not None and pulse.state == 'high' and pulse.src in want:
            if pulse.src not in highs:
                highs[pulse.src] = cycle

        if pulse.dst not in graph:
            continue

        node = graph[pulse.dst]
        if node.module['kind'] == 'broad':
            for edge in node.edges:
                q.put(Pulse('low', edge, pulse.dst))
        elif node.module['kind'] == 'ff':
            if pulse.state == 'low':
                node.module['state'] = not node.module['state']
                for edge in node.edges:
                    if node.module['state']:
                        q.put(Pulse('high', edge, pulse.dst))
                    else:
                        q.put(Pulse('low', edge, pulse.dst))
        elif node.module['kind'] == 'conj':
            if pulse.state == 'low':
                node.module['state'][pulse.src] = False
            else:
                node.module['state'][pulse.src] = True

            if all(v for v in node.module['state'].values()):
                for edge in node.edges:
                    q.put(Pulse('low', edge, pulse.dst))
            else:
                for edge in node.edges:
                    q.put(Pulse('high', edge, pulse.dst))
        else:
            assert False

    return ls, hs


def part1(lines):
    graph = parse(lines)

    tls, ths = 0, 0
    for _ in range(1000):
        ls, hs = sim(graph)
        tls += ls
        ths += hs

    return tls * ths


# simulate enough cycles to find when each of rx's
# parents send a high signal, then find the lcm
def part2(lines):
    graph = parse(lines)

    cycle = 0
    highs = {}
    for _ in range(10000):
        cycle += 1
        sim(graph, cycle, highs)

    return math.lcm(*highs.values())


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
