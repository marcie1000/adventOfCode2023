import re
# symbols: *-%/#&$=@+
# i rows, j columns

symb_pattern = re.compile(r"\+|\*|\-|\%|/|\#|\&|\$|\=|\@")
digit_pattern = re.compile(r"\d+")

def read_file():
    with open("input.txt") as f:
        txt = f.readlines()
        return(txt)

def read_all_symbols_pos(txt):
    s_pos = []
    i = 0
    for row in txt:
        j = 0
        for col in row:
            if(re.search(symb_pattern, col)):
                s_pos.append([i, j])
            j += 1
        i += 1
    return(s_pos)

def read_gear_symbols_pos(txt):
    s_pos = []
    i = 0
    for row in txt:
        j = 0
        for col in row:
            if(re.search(r"\*", col)):
                s_pos.append([i, j])
            j += 1
        i += 1
    return(s_pos)

# If there is other digits on the right and on the left, take them into account
def complete_number(txt, posi, posj, nb_rows, nb_cols):
    minj = posj
    maxj = posj

    # checks the i rows
    # leftchar
    cond = (minj > 0) and (txt[posi][minj - 1].isdigit())
    while(cond):
        minj -= 1
        cond = (minj > 0) and (txt[posi][minj - 1].isdigit())

    # rightchar
    cond = (maxj <= nb_cols) and (txt[posi][maxj + 1].isdigit())
    while(cond):
        maxj += 1
        cond = (maxj <= nb_cols) and (txt[posi][maxj + 1].isdigit())

    sub = txt[posi][minj:maxj+1]

    # deletes the numbers added to the sum from the text to avoid repeats
    txt[posi] = txt[posi][:minj] + ((maxj + 1 - minj) * '.') + txt[posi][maxj + 1:]
    return sub, txt

# Converts adjacent digits chars in a row in integers
def extract_numbers(s):
    l = re.findall(digit_pattern, s)
    add = 0
    li = []
    for i in l:
        if(i.isdigit()):
            li.append(int(i))
    return li

def search_adj_digit(txt, s_pos):
    add = 0
    nb_rows = len(txt)
    nb_cols = len(txt[0])

    for x in s_pos:

        pos_i = x[0]
        pos_j = x[1]

        sub, txt = complete_number(txt, pos_i-1, pos_j, nb_rows, nb_cols)
        add += sum(extract_numbers(sub))
        sub, txt = complete_number(txt, pos_i, pos_j, nb_rows, nb_cols)
        add += sum(extract_numbers(sub))
        sub, txt = complete_number(txt, pos_i+1, pos_j, nb_rows, nb_cols)
        add += sum(extract_numbers(sub))

    return add

def search_adj_digit_gears(txt, s_pos):
    add = 0
    nb_rows = len(txt)
    nb_cols = len(txt[0])

    for x in s_pos:

        pos_i = x[0]
        pos_j = x[1]

        rows = []

        sub, txt = complete_number(txt, pos_i-1, pos_j, nb_rows, nb_cols)
        rows += extract_numbers(sub)
        sub, txt = complete_number(txt, pos_i, pos_j, nb_rows, nb_cols)
        rows += extract_numbers(sub)
        sub, txt = complete_number(txt, pos_i+1, pos_j, nb_rows, nb_cols)
        rows += extract_numbers(sub)

        gear_ratio = 1
        if(len(rows) == 2):
            for i in rows:
                gear_ratio *= i
            add += gear_ratio
    return add

def part1():
    txt = read_file()
    s_pos = read_all_symbols_pos(txt)
    add = search_adj_digit(txt, s_pos)
    print("Part 1 : the sum of adjacent numbers is:", add)

def part2():
    txt = read_file()
    s_pos = read_gear_symbols_pos(txt)
    add = search_adj_digit_gears(txt, s_pos)
    print("Part 2 : the sum of gears ratios is:", add)

part1()
part2()

