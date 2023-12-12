import re

def readfile():
    with open("input.txt") as f:
        txt = f.readlines()
        return(txt)

def findall_int(needle, haystack):
    l = re.findall(needle, haystack)
    for i in range(len(l)):
        l[i] = int(l[i])
    return l

def getSublist(txt, line):
    #assert(re.findall(needle, txt[line]))
    sublist = []
    while(line < len(txt) and txt[line] != "\n"):
        sublist.append(findall_int(r"\d+", txt[line]))
        line += 1
    line += 1
    del sublist[0]
    return sublist, line

def convert(lst, mapl):
    it = 0
    for l in lst:
        for m in mapl:
            if(l >= m[1] and l < m[1] + m[2]):
                delta = m[1] - m[0]
                lst[it] -= delta
        it += 1
    return lst

def part1():
    print("Part 1: ", end="")
    txt = readfile()
    line = 0
    # read seeds list
    seeds = findall_int(r"\d+", txt[line])
    line += 2
    for i in range(7):
        mapp, line = getSublist(txt, line)
        seeds = convert(seeds, mapp)

    print("The lowest location number is:", min(seeds))

def testKeyOut(li):
    return(li[0])

def testKeyIn(li):
    return(li[1])

# Test every couple start of range/length of range in every map
# Modify values in couples through maps
# Subdivide couples if they don't fit in a single map bounds
def test(parsed, cpl):
    sortedIn = parsed.copy()
    sortedOut = parsed.copy()
    sortedIn.sort(key=testKeyIn)
    sortedOut.sort(key=testKeyOut)
    if sortedIn[0][1] > 0:
        sortedOut = [[0, 0, sortedIn[0][1]]] + sortedOut
        sortedIn = [[0, 0, sortedIn[0][1]]] + sortedIn
    minmax = []
    for m in sortedIn:
        minmax.append([m[1], m[1] + m[2] - 1, m[0], m[0] + m[2] - 1, - (m[1] - m[0])])

    i = 0
    for c in cpl:
        cplmin = c[0]
        cplmax = c[0] + c[1] - 1
        j = 0
        found = False
        while(not found and j < len(minmax)):
            minIn = minmax[j][0]
            maxIn = minmax[j][1]
            minOut = minmax[j][2]
            maxOut = minmax[j][3]
            delta = minmax[j][4]
            if(cplmin >= minIn and cplmin <= maxIn):
                cpl[i][0] += delta
                found = True
                if(cplmax > maxIn):
                    cpl[i][1] = maxIn - cplmin
                    cpl.append([maxIn + 1, cplmax - maxIn])
            j += 1
        i += 1
    return(cpl)

def part2():
    print("Part 2: ", end="")
    txt = readfile()
    line = 0
    # read seeds list
    seeds = findall_int(r"\d+", txt[line])
    cpl = []
    for i in range(0, len(seeds), 2):
        cpl.append([seeds[i], seeds[i + 1]])
    line += 2

    # Parse maps
    for i in range(7):
        mapp, line = getSublist(txt, line)
        cpl = test(mapp, cpl)

    mincpl = []
    for c in cpl:
        mincpl.append(c[0])

    print("The lowest location number is:", min(mincpl))

if(__name__ == "__main__"):
    part1()
    part2()

