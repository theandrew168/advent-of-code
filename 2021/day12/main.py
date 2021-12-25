from collections import Counter, defaultdict
import fileinput


def explore1(graph, path):
    start = path[-1]

    # check for dead ends
    if not graph[start]:
        yield path
        return

    # explore other paths
    for node in graph[start]:
        # skip if lower and already visited
        if node.islower() and node in path:
            continue

        # add node to path
        next_path = path.copy()
        next_path.append(node)

        # keep exploring
        yield from explore1(graph, next_path)


def should_skip(node, path):
    if not node.islower():
        return False

    if node not in path:
        return False

    c = Counter(n for n in path if n.islower() and n not in ['start', 'end'])
    counts = [e[1] for e in c.most_common()]
    if all(count == 1 for count in counts):
        return False

    return True


def explore2(graph, path):
    start = path[-1]

    # check for dead ends
    if not graph[start]:
        yield path
        return

    # explore other paths
    for node in graph[start]:
        # skip if lower and already visited
        if should_skip(node, path):
            continue

        # add node to path
        next_path = path.copy()
        next_path.append(node)

        # keep exploring
        yield from explore2(graph, next_path)


def part1(graph):
    paths = list(explore1(graph, ['start']))
    return sum(1 for p in paths if p[-1] == 'end')


def part2(graph):
    paths = list(explore2(graph, ['start']))
    return sum(1 for p in paths if p[-1] == 'end')


if __name__ == '__main__':
    # build out the graph
    graph = defaultdict(list)
    for line in fileinput.input():
        a, b = line.strip().split('-')
        if b != 'start':
            graph[a].append(b)
        if a != 'start':
            graph[b].append(a)

    # add empty node for end
    graph['end'] = []

    print(part1(graph))
    print(part2(graph))
