import math

def part1():
    timel = [52, 94, 75, 94]
    distl = [426, 1374, 1279, 1216]
    mul = 1

    for r in range(len(timel)):
        delta = float(timel[r] ** 2 - 4 * - 1 * - distl[r])
        x1 = round(( - timel[r] + math.sqrt(delta)) / 2 * - 1)
        x2 = round(( - timel[r] - math.sqrt(delta)) / 2 * - 1)
        if x1 < x2:
            mul *= timel[r] - (x1 * 2 + 1)
        else:
            mul *= timel[r] - (x2 * 2 + 1)


    print("Part 1: the result is", mul)

def part2():
    timeRef = 52947594
    distRef = 426137412791216

    delta = float(timeRef ** 2 - 4 * - 1 * - distRef)
    x1 = round(( - timeRef + math.sqrt(delta)) / 2 * - 1)
    x2 = round(( - timeRef - math.sqrt(delta)) / 2 * - 1)
    res = 0
    if x1 < x2:
        res = timeRef - (x1 * 2 + 1)
    else:
        res = timeRef - (x2 * 2 + 1)

    print("Part 2: the result is", res)

part1()
part2()
