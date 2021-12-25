import fileinput


def flip_x(rows):
    flipped = []
    for row in rows:
        flipped.append(row[::-1])
    return flipped


def flip_y(rows):
    return rows[::-1]


class Paper():

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rows = []
        for _ in range(height):
            row = [0] * width
            self.rows.append(row)

    def __str__(self):
        s = ''
        for row in self.rows:
            r = ''.join('#' if n > 0 else '.' for n in row)
            s += r + '\n'
        return s[:-1]

    def dot(self, x, y):
        self.rows[y][x] += 1

    def fold_x(self, x):
        # split page, flip right
        left = []
        for row in self.rows:
            left.append(row[:x])

        right = []
        for row in self.rows:
            right.append(row[x + 1:])

        right = flip_x(right)

        # pad left and right to make em match
        while len(left[0]) < len(right[0]):
            for row in left:
                row.insert(0, 0)
        while len(right[0]) < len(left[0]):
            for row in right:
                row.insert(0, 0)

        # merge left and right
        rows = []
        for y in range(self.height):
            row = []
            for x in range(len(left[0])):
                row.append(left[y][x] + right[y][x])
            rows.append(row)

        # return the new page
        page = Paper(len(rows[0]), self.height)
        page.rows = rows
        return page

    def fold_y(self, y):
        # split page, flip bottom
        top, bot = self.rows[:y], self.rows[y + 1:]
        bot = flip_y(bot)

        # pad top and bottom to make em match
        while len(bot) < len(top):
            bot.insert(0, [0] * self.width)
        while len(top) < len(bot):
            top.insert(0, [0] * self.width)

        # merge top and bottom
        rows = []
        for y in range(len(top)):
            row = []
            for x in range(self.width):
                row.append(top[y][x] + bot[y][x])
            rows.append(row)

        # return the new page
        page = Paper(self.width, len(rows))
        page.rows = rows
        return page


def part1(points, folds):
    # determine initial width and height
    width = 0
    height = 0
    for x, y in points:
        if x > width:
            width = x
        if y > height:
            height = y

    # create the page
    page = Paper(width + 1, height + 1)
    for x, y in points:
        page.dot(x, y)

    # apply folds
    for axis, n in folds:
        if axis == 'x':
            page = page.fold_x(n)
        else:
            page = page.fold_y(n)
        break

    answer = 0
    for row in page.rows:
        answer += sum(1 for d in row if d > 0)
    return answer


def part2(points, folds):
    # determine initial width and height
    width = 0
    height = 0
    for x, y in points:
        if x > width:
            width = x
        if y > height:
            height = y

    # create the page
    page = Paper(width + 1, height + 1)
    for x, y in points:
        page.dot(x, y)

    # apply folds
    for axis, n in folds:
        if axis == 'x':
            page = page.fold_x(n)
        else:
            page = page.fold_y(n)

    return str(page)


if __name__ == '__main__':
    points = []
    folds = []
    for line in fileinput.input():
        line = line.strip()
        if len(line) == 0:
            continue

        if ',' in line:
            x, y = line.split(',')
            x, y = int(x), int(y)
            points.append((x, y))
        else:
            fold = line.split()[-1]
            axis, n = fold.split('=')
            n = int(n)
            folds.append((axis, n))

    print(part1(points, folds))
    print(part2(points, folds))
