import fileinput


class Node:

    def __init__(self, parent=None):
        self.parent = parent

        self.left = None
        self.right = None

    def __str__(self):
        s = '[{},{}]'
        return s.format(self.left, self.right)


def list_to_tree(lst, parent=None):
    if isinstance(lst, int):
        return lst

    n = Node(parent)
    n.left = list_to_tree(lst[0], n)
    n.right = list_to_tree(lst[1], n)

    return n


def reduce(number, depth=0):
    # split
    if isinstance(number, int):
        if number >= 10:
            print('split')
        return number

    # explode
    if depth >= 4:
        print('explode')

    print(number, depth)

    # recur
    number.left = reduce(number.left, depth + 1)
    number.right = reduce(number.right, depth + 1)
    return number


def add(a, b):
    n = Node()
    n.left = a
    n.right = b
    n.left.parent = n
    n.right.parent= n

    n = reduce(n)
    return n


def part1(numbers):
    answer = numbers[0]
    for number in numbers[1:]:
        answer = add(answer, number)
    return answer


def part2(numbers):
    pass


if __name__ == '__main__':
    numbers = []
    for line in fileinput.input():
        lst = eval(line.strip())
        number = list_to_tree(lst)
        numbers.append(number)

    print(part1(numbers))
    print(part2(numbers))
