import re

def readfile():
    with open("input.txt") as f:
        txt = f.readlines()
    return txt

def findGalPos(txt):
    gal = []
    cnt = 0
    for i in range(len(txt)):
        for j in range(len(txt[0])):
            if(txt[i][j] == '#'):
                gal.append([j, i, cnt])
                cnt += 1
    return gal

def calcPair(pos1, pos2):
    deltax = abs(pos1[0] - pos2[0])
    deltay = abs(pos1[1] - pos2[1])
    return deltax + deltay

def calcPaths(gal):
    cnt = 0
    nbgal = len(gal)
    add = 0
    for i in range(nbgal):
        for j in (range(i + 1, nbgal)):
            add += calcPair( gal[i], gal[j])
            cnt += 1
    return add

def resizeCol(txt, gal, q):
    q -= 1
    i = 0
    add = 0
    while(i < len(txt[0]) - 1):
        found = False
        j = 0
        while(j < len(txt) and not found):
            if(txt[j][i] == '#'):
                found = True
            j += 1
        if(not found):
            #breakpoint()
            for k in range(len(gal)):
                if(gal[k][0] >= i + add):
                    gal[k][0] += q
            add += q
        i += 1
    return gal

def resizeRow(txt, gal, q):
    q -= 1
    i = 0
    add = 0
    while(i < len(txt)):
        if(not re.search('#', txt[i])):
            #breakpoint()
            for k in range(len(gal)):
                if(gal[k][1] >= i + add):
                    gal[k][1] += q
            add += q
        i += 1
    return gal

def resize(txt, gal, q):
    gal = resizeRow(txt, gal, q)
    gal = resizeCol(txt, gal, q)
    return gal

if __name__ == "__main__":
    txt = readfile()
    gal = findGalPos(txt)
    gal = resize(txt, gal, 2)
    print("PART 1: the sum is:", calcPaths(gal))

    gal = findGalPos(txt)
    gal = resize(txt, gal, 1000000)
    print("PART 2: the sum is:", calcPaths(gal))


