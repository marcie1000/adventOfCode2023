import re

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
        n = 0
        while(n < len(nodes) and nodes[n] != stofind):
            n += 1
        pos = n
        lr_it += 1
        cnt += 1
        if(lr_it >= len(lrList) - 1):
            lr_it = 0
        if(nodes[pos] == "ZZZ"):
            quit = True
    print("Part 1: the number of steps is", cnt)

if __name__ == "__main__":
    part1()
