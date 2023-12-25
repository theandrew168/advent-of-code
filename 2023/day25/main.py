from collections import defaultdict
import fileinput
import math
import queue


def parse(lines):
    g = defaultdict(set)
#    print('graph G {')
    for line in lines:
        k, vs = line.split(': ')
        vs = vs.split()
        for v in vs:
            g[k].add(v)
            g[v].add(k)
#            print(k, '--', v, '[ tooltip="{} {}" ];'.format(k, v))
#    print('}')
    return g


def count(graph, start):
    seen = set()

    q = queue.Queue()
    q.put(start)

    cnt = 0
    while not q.empty():
        node = q.get()
        if node in seen:
            continue

        seen.add(node)
        cnt += 1

        for edge in graph[node]:
            q.put(edge)

    return cnt


def part1(lines):
    g = parse(lines)

    # determined via visual graph analysis
#    cuts = [('hfx', 'pzl'), ('bvb', 'cmg'), ('nvd', 'jqt')]
    cuts = [('qqh', 'xbl'), ('dsr', 'xzn'), ('tbq', 'qfj')]
    for k, v in g.items():
        for a, b in cuts:
            if k == a and b in v:
                v.remove(b)
            if k == b and a in v:
                v.remove(a)

    counts = set()
    for k in list(g):
        cnt = count(g, k)
        counts.add(cnt)
        if len(counts) > 1:
            break

    return math.prod(counts)


def part2(lines):
    return 'Merry Christmas!'


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
