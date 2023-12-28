import re

def readfile():
    with open("input.txt") as f:
        txt = f.readlines()
    return txt

def expandCol(txt):
    i = 0
    while(i < len(txt[0]) - 1):
        found = False
        j = 0
        while(j < len(txt) and not found):
            if(txt[j][i] == '#'):
                found = True
            j += 1
        if(not found):
            j = 0
            while(j < len(txt)):
                txt[j] = txt[j][:i] + '.' + txt[j][i:]
                j += 1
            i += 1
        i += 1
    return txt


def expandRow(txt):
    i = 0
    while(i < len(txt)):
        if(not re.search('#', txt[i])):
            txt = txt[:i] + ['.' * (len(txt[i]) - 1) + '\n'] + txt[i:]
            i += 1
        i += 1
    return txt

def findGalPos(txt):
    gal = []
    for i in range(len(txt)):
        for j in range(len(txt[0])):
            if(txt[i][j] == '#'):
                gal.append([j, i])
    return gal

def calcPair(gal, pos1, pos2):
    deltax = abs(pos1[0] - pos2[0])
    deltay = abs(pos1[1] - pos2[1])
    return deltax + deltay

def calcPaths(gal):
    cnt = 0
    nbgal = len(gal)
    add = 0
    for i in range(nbgal):
        for j in (range(i + 1, nbgal)):
            add += calcPair(gal, gal[i], gal[j])
            cnt += 1
    return add

if __name__ == "__main__":
    txt = readfile()
    txt = expandRow(txt)
    txt = expandCol(txt)
    gal = findGalPos(txt)
    print("PART 1: the sum is:", calcPaths(gal))


