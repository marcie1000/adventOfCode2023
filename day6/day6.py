def part1():
    timel = [52, 94, 75, 94]
    distl = [426, 1374, 1279, 1216]
    mul = 1

    for r in range(len(timel)):
        mid = timel[r] // 2
        i = 1
        dist = 0
        while(i < mid and dist <= distl[r]):
            dist = (timel[r] - i) * i
            i += 1
        i -= 1
        mul *= (timel[r] - 2 * i + 1)
    print("Part 1: the result is", mul)

def part2():
    timeRef = 52947594
    distRef = 426137412791216
    mid = timeRef // 2

    i = 1
    dist = 0
    while(i < mid and dist <= distRef):
        dist = (timeRef - i) * i
        i += 100
    i -= 1
    while(i > 0 and dist > distRef):
        dist = (timeRef - i) * i
        i -= 1
    i += 2
    print("Part 2: the result is", (timeRef - 2 * i + 1))

part1()
part2()
