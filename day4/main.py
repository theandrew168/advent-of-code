import fileinput

class Board:

    def __init__(self, numbers, size=5):
        if len(numbers) != size * size:
            raise ValueError('invalid board')

        self.numbers = list(numbers)
        self.markers = [False] * len(self.numbers)
        self.size = size

    def __str__(self):
        s = ''
        for i in range(self.size):
            start = i * self.size
            end = start + self.size
            row = self.numbers[start:end]
            s += ' '.join(str(n) for n in row)
            s += '\n'

        return s

    def __contains__(self, item):
        return item in self.numbers

    def is_winner(self):
        # check rows
        for i in range(self.size):
            start = i * self.size
            end = start + self.size
            row = self.markers[start:end]
            if all(row):
                return True

        # check cols
        for i in range(self.size):
            start = i
            end = self.size * (self.size - 1) + i
            step = self.size
            col = self.markers[start:end:step]
            if all(col):
                return True

        # check diag

    def mark(self, number):
        if number not in self:
            return False
        idx = self.numbers.index(number)
        self.markers[idx] = True
        return True

    def marked_unmarked(self):
        marked = []
        unmarked = []
        for i, marker in enumerate(self.markers):
            number = self.numbers[i]
            if marker:
                marked.append(number)
            else:
                unmarked.append(number)

        return marked, unmarked


def part1(numbers, boards):
    print(numbers)
    for board in boards:
        print(board)


def part2():
    pass


if __name__ == '__main__':
    numbers = []
    boards = []

    board_numbers = None
    for i, line in enumerate(fileinput.input()):
        if i == 0:
            numbers = [int(n) for n in line.strip().split(',')]
            continue

        # check for blank line to start new board
        if len(line.strip()) == 0:
            if board_numbers is not None:
                board = Board(board_numbers)
                boards.append(board)
            board_numbers = []
            continue

        board_numbers.extend(int(n) for n in line.strip().split())

    # finish final board
    board = Board(board_numbers)
    boards.append(board)

    print(part1(numbers, boards))
    print(part2())
