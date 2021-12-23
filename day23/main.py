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
SLOTS = [3, 5, 7, 1, 9, 0, 10]

BURROW = """
#############
#{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#
  #########
"""


class State:

    def __init__(self, hall, rooms, energy=0, prev=None):
        self.hall = hall
        self.rooms = rooms

        self.energy = energy
        self.prev = prev

    @property
    def solved(self):
        want = [['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']]
        return str(self.rooms) == str(want)

    def __str__(self):
        hall = ''.join(slot or '.' for slot in self.hall)
        r00 = self.rooms[0][0] or '.'
        r01 = self.rooms[0][1] or '.'
        r10 = self.rooms[1][0] or '.'
        r11 = self.rooms[1][1] or '.'
        r20 = self.rooms[2][0] or '.'
        r21 = self.rooms[2][1] or '.'
        r30 = self.rooms[3][0] or '.'
        r31 = self.rooms[3][1] or '.'

        s = BURROW.format(hall, r00, r10, r20, r30, r01, r11, r21, r31)
        return s.strip()

    def __hash__(self):
        return hash((str(self.hall), str(self.rooms)))

    def __lt__(self, other):
        return self.energy < other.energy

    # yield out all possible moves from the given state
    def __iter__(self):
        blocks = [slot for slot in SLOTS if self.hall[slot]]

        if self.solved:
            raise StopIteration

        # room to hall
        for ri, room in enumerate(self.rooms):
            entry = (ri + 1) * 2

            # room is done
            if all(r == ROOMS[ri] for r in room):
                continue

            for ai, amph in enumerate(room):
                # room spot is empty
                if not amph:
                    continue
                # amph is blocked into their room
                if ai == 1 and room[0]:
                    continue
                # amph is in the correct spot
                if ai == 1 and room[1] == ROOMS[ri]:
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

                    yield State(hall, rooms, energy, prev=self)

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

                ai = 0 if room[1] else 1
                hall = [h for h in self.hall]
                hall[slot] = None
                rooms = [r.copy() for r in self.rooms]
                rooms[ri][ai] = amph

                dist = (ai + 1) + abs(slot - entry)
                energy = dist * COSTS[amph]
                energy = self.energy + energy

                yield State(hall, rooms, energy, prev=self)


# treat this sort of like Dijkstra's
# tracing out the tree of potential moves
# updating similar states if the energy cost is lower
# somehow keep a ref to previous move
def solve(state):
    pq = PriorityQueue()
    pq.put((0, state))

    # keep track of the best ways to reach each game state
    best = {}
    best[state] = 0

    visited = set()
    while not pq.empty():
        e, s = pq.get()
        visited.add(s)
        for ns in s:
            if ns in visited:
                continue
            print(s)
            print(ns)
            print()
            total = best[s] + ns.energy
            if ns not in best or total < best[ns]:
                pq.put((total, ns))
                best[ns] = total

    idx = [i for i in best if best[i].solved][0]
    return best[idx]


def part1(state):
    return solve(state)


def part2(state):
    pass


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
    print(part2(state))
