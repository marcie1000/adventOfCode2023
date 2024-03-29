import re

def readFile():
    with open("input.txt") as f:
        txt = f.readlines()
        return txt

def extractNumbers(txt):
    numbers = []
    # rex = []
    for t in txt:
        # regex = re.finditer(r"[?#]+", t)
        nb = re.findall(r"\d+", t)
        for i in range(len(nb)):
            nb[i] = int(nb[i])
        numbers.append(nb)
        # rg = []
        # for r in regex:
        #     rg.append([r.start(), len(r.group())])
        # rex.append(rg)
    return numbers


def stats(numbers, ln):
    qmarks = ln.count('?')
    sharps = ln.count('#')
    dots = ln.count('.')
    total = qmarks + sharps + dots
    damaged = sum(numbers)
    oper = total - damaged
    seq = ln[:ln.find(' ')]
    shToFind = damaged - sharps
    dotToFind = oper - dots
    st = {"seq": seq, "shToFind": shToFind, "dotToFind": dotToFind}
    # st = {"qumarks": qmarks, "sharps": sharps, "dots": dots,
    #       "total": total, "damaged": damaged, "oper": oper,
    #       "seq": seq, "shToFind": shToFind, "dotToFind": dotToFind}
    return st

def tryToGuessNumbers(seq):
    stop = seq.find('?')
    if(stop == -1):
        stop = None
    ls = re.findall(r"\#+", seq[:stop])
    res = []
    for l in ls:
        res.append(len(l))
    return res

def replaceChar(source, i, c):
    return source[:i] + c + source[i+1:]

# Test if a '.' or a '#' would be possible at pos i
def testchar(sc, i, c, numbers):
    if(c == '.' and sc["dotToFind"] == 0):
        return False
    if(c == '#' and sc["shToFind"] == 0):
        return False
    seqtest = replaceChar(sc["seq"], i, c)
    guess = tryToGuessNumbers(seqtest)
    j = 0
    for g in range(len(guess)):
        if(len(guess) > len(numbers)):
            return False
        if(guess[g] > numbers[g]):
            return False
        if(len(guess) == 0):
            return True
        if(len(guess) - 1 > g and guess[g] != numbers[g]):
            return False
    return True

def decideNewScenar(scenars, s, i, numbers):
    sc = scenars[s]
    boolsh = testchar(sc, i, '#', numbers)
    booldot = testchar(sc, i, '.', numbers)
    add = boolsh + booldot
    # print("add", add)
    reld = False
    if(add == 2):
        scenars.append(sc.copy())
        sc["seq"] = replaceChar(sc["seq"], i, '#')
        sc["shToFind"] -= 1
        l = len(scenars)
        scenars[l-1]["seq"] = replaceChar(scenars[l-1]["seq"], i, '.')
        scenars[l-1]["dotToFind"] -= 1
    elif(boolsh):
        sc["seq"] = replaceChar(sc["seq"], i, '#')
        sc["shToFind"] -= 1
    elif(booldot):
        sc["seq"] = replaceChar(sc["seq"], i, '.')
        sc["dotToFind"] -= 1
    else:
        scenars.pop(s)
        reld = True
        s = 0
        i = 0
    return scenars, s, i, reld

def scenarios(stat, numbers):
    scenars = [stat]
    s = 0 # scenario id / iterator
    # cnt = 0
    while(s < len(scenars)):
        reld = False
        sc = scenars[s]
        i = 0
        while(i < len(sc["seq"]) and not reld):
            if(sc["seq"][i] == '?'):
                # breakpoint()
                scenars, s, i, reld = decideNewScenar(scenars, s, i, numbers)
                # for a in scenars:
                #     print("scenar ::::::::", len(scenars), a["seq"], "s", s, "i", i, numbers, cnt)
                #     cnt += 1
                # print("")
            if(not reld):
                i += 1
        if(not reld):
            s += 1
    # print("The len of scenar is", len(scenars))
    lasttwo = [0,0,0,0]
    for e in scenars:
        if(e["seq"][-2:] == ".."):
            lasttwo[0] += 1
        if(e["seq"][-2:] == ".?"):
            lasttwo[1] += 1
        if(e["seq"][-2:] == "?"):
            lasttwo[2] += 1
        if(e["seq"][-2:] == "??"):
            lasttwo[3] += 1

    return len(scenars), lasttwo

def processRowsP1(numbers, txt):
    add = 0
    resultsP1 = []
    lasttwo = []
    for i in range(len(txt)):
        stat = stats(numbers[i], txt[i])
        result, lttemp = scenarios(stat, numbers[i])
        lasttwo.append(lttemp)
        add += result
        resultsP1.append(result)
    print("Part 1: the sum of possibilities is", add)
    return(resultsP1, lasttwo)

def processRowsP2(numbers, txt, resultsP1, lasttwo):
    # breakpoint()
    value = 2
    add = 0
    l = len(txt)
    for i in range(l):
        # numbers[i] = numbers[i] * value
        stat = stats(numbers[i], txt[i])
        # print("entry: stat=", stat, "numbers[i]=", numbers[i])
        numbers[i] = numbers[i] * value
        stat["seq"] = (stat["seq"] + '?') * value
        # print("before", stat["seq"])
        stat["seq"] = stat["seq"][:-1] + ' '
        # stat["seq"] = stat["seq"] + '?' + stat["seq"]

        stat = stats(numbers[i], stat["seq"])
        print("Part 2: processing (", i / l * 100, " %)", sep="", end="\r")
        # print("after ", stat["seq"])
        # stat["shToFind"] *= value
        # stat["dotToFind"] *= value

        # print("after: stat=", stat, "numbers[i]=", numbers[i])
        # print(stat["seq"], numbers[i])
        # breakpoint()
        result = scenarios(stat, numbers[i])
        # print(result, end=" ")
        result = result // resultsP1[i]
        result = resultsP1[i] * (result ** 4)
        # print(result, resultsP1[i])
        add += result
        # print(result)
    print("Part 2: the sum of possibilities is", add)

if __name__ == "__main__":
    txt = readFile()
    extractNumbers(txt)
    numbers = extractNumbers(txt)
    resultsP1, lasttwo = processRowsP1(numbers, txt)
    # processRowsP2(numbers, txt, resultsP1, lasttwo)
    print(lasttwo)
