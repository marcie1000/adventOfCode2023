COLORS = ["red", "green", "blue"]
QUANTITY = [12, 13, 14]

def read_game_id(ln):
    return int((re.search(r"\d+", ln)[0]))

def extract_max_color_nb(ln, colorID):
    # gives a list like ['1 green', '1 green', '5 green', '1 green']
    c_plus_nb = re.findall(r"\d+ " + COLORS[colorID], ln)

    # gives something like [1, 1, 5, 1]
    c = []
    for x in c_plus_nb:
        c.append(int(re.search(r"\d+", x)[0]))

    return max(c)

def part_one():
    with open("input.txt") as f:
        sum = 0
        for ln in f:
            game_id = read_game_id(ln)
            gameOK = True
            for i in range(0, 3):
                if (QUANTITY[i] < extract_max_color_nb(ln, i)):
                    gameOK = False
            sum += (gameOK * game_id)
        print("Part One : sum of correct games is:", sum)

def part_two():
    with open("input.txt") as f:
        sum = 0
        for ln in f:
            power = 1
            for i in range(0, 3):
                power *= extract_max_color_nb(ln, i)
            sum += power
        print("Part Two : sum of powers is:", sum)

import re
with open("input.txt") as f:
    part_one()
    part_two()
