import re

def readFile():
    with open("input.txt") as f:
        txt = f.readlines()
        return(txt)

def splitParts(txt):
    winNumS = []
    myNumS = []
    for l in txt:
        winNumS.append(l[9:40])
        myNumS.append(l[41:])
    return winNumS, myNumS

def extractNumbers(biglistS):
    biglistI = []
    for i in biglistS:
        li = []
        ls = re.findall(r"\d+", i)
        for j in ls:
            li.append(int(j))
        biglistI.append(li)
    return biglistI

def calcPoints(win, my):
    i = 0
    add = 0
    for wincard in win:
        cardGoodNum = 0
        j = 0
        for w in wincard:
            if w in my[i]:
                cardGoodNum += 1
        if(cardGoodNum != 0):
            add += 2 ** (cardGoodNum - 1)
        i += 1
    return add

def cardCopies(win, my):
    qCard = [1] * 198
    i = 0
    for wincard in win:
        cardGoodNum = 0
        for w in wincard:
            if w in my[i]:
                cardGoodNum += 1
        for j in range(1, cardGoodNum + 1):
            qCard[i + j] += qCard[i]
        i += 1

    # print number of each card
    # print(qCard)
    return sum(qCard)


txt = readFile()
winNumS, myNumS = splitParts(txt)
totalCards = len(winNumS)
winNumI = extractNumbers(winNumS)
myNumI = extractNumbers(myNumS)
add = calcPoints(winNumI, myNumI)
print("Part 1: the total number of points is :", add)
add = cardCopies(winNumI, myNumI)
print("Part 2: the total number of cards is :", add)


