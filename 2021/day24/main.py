import fileinput


# x = !(z % 26 + v2 == input)
# z = (z / v1)      (1 or 26)
# y = 25 * x + 1
# z = z * y
# y = (input + v3) * x
# z = z + y
#
# x = z % 26 + v2 != input
# z = z // v1   (1 or 26)
# z = z * (25 * x + 1)
# z = z + ((input + v3) * x)
def sim(i, z, v1, v2, v3):
    x = ((z % 26) + v2) != i
    z = z // v1
    z = z * (25 * x + 1)
    z = z + ((i + v3) * x)
    return z


# try each input 1-9
# if sim z is in the next set, try the recur
# if recur hits the bottom, valid model number
def code(zi, model, params, wants):
    print(model)
    # hit the buttom, return back up
    if len(params) <= 1:
        print('MODEL NUMBER:', model)
        return

    # prep the params for this digit
    v1, v2, v3 = params[0]

    # try in input number (1-9)
    for i in range(9, 0, -1):
        res = sim(i, zi, v1, v2, v3)
        # check if z is in the acceptable set for the next prog
        if res in wants[1]:
            code(res, model + str(i), params[1:], wants[1:])


def part1(lines):
    progs = []
    for line in lines:
        if line.startswith('inp'):
            progs.append([line])
        else:
            progs[-1].append(line)

    params = []
    for prog in progs:
        v1 = int(prog[4].split()[-1])
        v2 = int(prog[5].split()[-1])
        v3 = int(prog[15].split()[-1])
        params.append((v1, v2, v3))

    print('shf chk add')
    for param in params:
        print(param)

    return 42

    want = set()
    want.add(0)
    wants = [want]
    for v1, v2, v3 in reversed(params):
        print('solving', len(wants) - 1)
        want = wants[-1]
        zs = set()
        for i in range(1, 10):
            for z in range(10**6):
                res = sim(i, z, v1, v2, v3)
                if res in want:
                    zs.add(z)
        wants.append(zs)

    wants = wants[:-1]
    wants = reversed(wants)
    wants = list(wants)
#    return code(0, '', params, wants)
    return 42


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print('Did this one by hand!')
