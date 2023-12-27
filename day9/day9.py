import re

def readfile():
    with open("input.txt") as f:
        txt = f.readlines()
    return txt

def extractNumbers(ln):
    li = re.findall(r"-?\d+", ln)
    nb = []
    for l in li:
        nb.append(int(l))
    return nb

def calcDiffs(li):
    newLevel = []
    for i in range(len(li) - 1):
        newLevel.append(li[i + 1] - li[i])
    return newLevel

def predictForwards(nb):
    nb[-1].append(0)
    for i in reversed(range(1, len(nb))):
        # add the predicted value to the previous level
        nb[i - 1].append(nb[i - 1][-1] + nb[i][-1])
    return(nb[0][-1])

def predictBackwards(nb):
    nb[-1].append(0)
    for i in reversed(range(1, len(nb))):
        # sub the predicted value to the previous level
        nb[i - 1] = [nb[i - 1][0] - nb[i][0]] + nb[i - 1]
    return(nb[0][0])

if(__name__ == "__main__"):
    txt = readfile()
    addF = 0
    addB = 0
    for t in txt:
        nb = [extractNumbers(t)]
        i = 0
        while(sum(nb[i]) != 0 and len(nb[i]) > 0):
            nb.append(calcDiffs(nb[i]))
            i += 1
        #print(nb)
        addF += predictForwards(nb)
        addB += predictBackwards(nb)
    print("Part 1:", addF)
    print("Part 2:", addB)
