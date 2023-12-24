import math

def readfile():
    with open("input.txt") as f:
        txt = f.readlines()
        return txt

def parse(txt):
    nodes=[]
    netl=[]
    netr=[]
    for t in txt[2:]:
        nodes.append(t[:3])
        netl.append(t[7:10])
        netr.append(t[12:15])
    return nodes, netl, netr

def searchS(stofind, nodes):
    n = 0
    while(n < len(nodes) and nodes[n] != stofind):
        n += 1
    return n

def part1():
    txt = readfile()
    lrList = txt[0]
    nodes, netl, netr = parse(txt)

    # search "AAA"
    n = 0
    while(n < len(nodes) and nodes[n] != "AAA"):
        n += 1
    pos = n

    cnt = 0
    lr = ""
    lr_it = 0
    quit = False
    while(not quit):
        lr = lrList[lr_it]
        stofind = ""
        if(lr == 'L'):
            stofind = netl[pos]
        else:
            stofind = netr[pos]
        pos = searchS(stofind, nodes)
        lr_it += 1
        cnt += 1
        if(lr_it >= len(lrList) - 1):
            lr_it = 0
        if(nodes[pos] == "ZZZ"):
            quit = True
    print("Part 1: the number of steps is", cnt)



def part2():
    txt = readfile()
    lrList = txt[0]
    nodes, netl, netr = parse(txt)

    pos = []
    # search "**A"
    for n in range(len(nodes)):
        if(nodes[n][2] == 'A'):
            pos.append(n)

    steps = []
    i = 0
    for p in pos:
        cnt = 0
        lr = ""
        lr_it = 0
        quit = False
        print("                                            ", end='\r')
        print("Part 2: processing... (", round(i/len(pos)*100), "%)", sep='', end='\r')
        while(not quit):
            quit = True
            lr = lrList[lr_it]
            stofind = ""
            if(lr == 'L'):
                stofind = netl[p]
            else:
                stofind = netr[p]
            p = searchS(stofind, nodes)
            if(nodes[p][2] != 'Z'):
                quit = False
            lr_it += 1
            cnt += 1
            if(lr_it >= len(lrList) - 1):
                lr_it = 0
        steps.append(cnt)
        i += 1
    print("Part 2: the number of steps is", math.lcm(*steps))

if __name__ == "__main__":
    part1()
    part2()
