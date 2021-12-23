import fileinput
from functools import cache
from queue import PriorityQueue

# movement costs
COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

# room designations
ROOMS = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
}

# hallway slots
SLOTS = [0, 1, 3, 5, 7, 9, 10]


class State:

    def __init__(self, hall, rooms, energy=0):
        self.hall = hall
        self.rooms = rooms
        self.energy = energy

    @property
    def solved(self):
        size = len(self.rooms[0])
        want = [['A'] * size, ['B'] * size, ['C'] * size, ['D'] * size]
        return str(self.rooms) == str(want)

    def __str__(self):
        lines = [
            '#############',
        ]

        hall = ''.join(slot or '.' for slot in self.hall)
        lines.append('#' + hall + '#')

        for i in range(len(self.rooms[0])):
            s = '###{}#{}#{}#{}###' if i == 0 else '  #{}#{}#{}#{}#'
            r0 = self.rooms[0][i] or '.'
            r1 = self.rooms[1][i] or '.'
            r2 = self.rooms[2][i] or '.'
            r3 = self.rooms[3][i] or '.'
            s = s.format(r0, r1, r2, r3)
            lines.append(s)

        lines.append('  #########')
        return '\n'.join(lines)

    def __lt__(self, other):
        return self.energy < other.energy

    # yield out all possible moves from the given state
    def __iter__(self):
        blocks = [slot for slot in SLOTS if self.hall[slot]]

        if self.solved:
            return

        # hall to room
        for slot, amph in enumerate(self.hall):
            # hall spot is empty
            if not amph:
                continue

            for ri, room in enumerate(self.rooms):
                entry = (ri + 1) * 2
                want = ROOMS[ri]
                dont = list(ROOMS.values())
                dont.remove(want)

                # not the correct room for this amph
                if amph != want:
                    continue
                # room contains incorrect amphs
                if any(s in dont for s in room):
                    continue

                # check for blocks (right)
                if any(b < slot and b > entry for b in blocks):
                    continue
                # check for blocks (left)
                if any(b > slot and b < entry for b in blocks):
                    continue

                if want in room:
                    ai = room.index(want) - 1
                else:
                    ai = len(self.rooms[0]) - 1
                hall = [h for h in self.hall]
                hall[slot] = None
                rooms = [r.copy() for r in self.rooms]
                rooms[ri][ai] = amph

                dist = (ai + 1) + abs(slot - entry)
                energy = dist * COSTS[amph]
                energy = self.energy + energy

                yield State(hall, rooms, energy)

        # room to hall
        for ri, room in enumerate(self.rooms):
            entry = (ri + 1) * 2

            # room is done for now
            if all(r == ROOMS[ri] for r in room if r):
                continue

            for ai, amph in enumerate(room):
                # room spot is empty
                if not amph:
                    continue
                # amph is blocked into their room
                if any(ai == i + 1 and room[i] for i in range(len(self.rooms) - 1)):
                    continue

                # try each possible hallway slot
                for slot in SLOTS:
                    # hall spot is taken
                    if self.hall[slot]:
                        continue
                    # check for blocks (right)
                    if any(b < slot and b > entry for b in blocks):
                        continue
                    # check for blocks (left)
                    if any(b > slot and b < entry for b in blocks):
                        continue

                    hall = [h for h in self.hall]
                    hall[slot] = amph
                    rooms = [r.copy() for r in self.rooms]
                    rooms[ri][ai] = None

                    dist = (ai + 1) + abs(slot - entry)
                    energy = dist * COSTS[amph]
                    energy = self.energy + energy

                    yield State(hall, rooms, energy)


# treat this sort of like Dijkstra's
# tracing out the tree of potential moves
# updating similar states if the energy cost is lower
def solve(state):
    pq = PriorityQueue()
    pq.put((0, state))

    # keep track of the best ways to reach each game state
    best = {}
    best[str(state)] = 0

    visited = set()
    while not pq.empty():
        e, s = pq.get()
        visited.add(str(s))
        for ns in s:
            if str(ns) in visited:
                continue
            total = ns.energy
            if str(ns) not in best or total < best[str(ns)]:
                pq.put((total, ns))
                best[str(ns)] = total

    return best


def part1(state):
    best = solve(state)

    hall = [None,] * 11
    r1 = ['A', 'A']
    r2 = ['B', 'B']
    r3 = ['C', 'C']
    r4 = ['D', 'D']
    want = State(hall, [r1, r2, r3, r4])

    return best[str(want)]


def part2(state):
    best = solve(state)

    hall = [None,] * 11
    r1 = ['A', 'A', 'A', 'A']
    r2 = ['B', 'B', 'B', 'B']
    r3 = ['C', 'C', 'C', 'C']
    r4 = ['D', 'D', 'D', 'D']
    want = State(hall, [r1, r2, r3, r4])

    return best[str(want)]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    hall = [None,] * 11

    r1 = [lines[2][3], lines[3][3]]
    r2 = [lines[2][5], lines[3][5]]
    r3 = [lines[2][7], lines[3][7]]
    r4 = [lines[2][9], lines[3][9]]
    state = State(hall, [r1, r2, r3, r4])
    print(part1(state))

    r1 = [r1[0], 'D', 'D', r1[1]]
    r2 = [r2[0], 'C', 'B', r2[1]]
    r3 = [r3[0], 'B', 'A', r3[1]]
    r4 = [r4[0], 'A', 'C', r4[1]]
    state2 = State(hall, [r1, r2, r3, r4])
    print(part2(state2))
