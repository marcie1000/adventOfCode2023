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

def getSublist(needle, txt, line):
    assert(re.findall(needle, txt[line]))
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

txt = readfile()
line = 0

# read seeds list

seeds = findall_int(r"\d+", txt[line])

line += 2

# Parse maps

seedsToSoil, line = getSublist("seed-to-soil map:", txt, line)
soilToFertilizer, line = getSublist("soil-to-fertilizer map:", txt, line)
fertilizerToWater, line = getSublist("fertilizer-to-water map:", txt, line)
waterToLight, line = getSublist("water-to-light map:", txt, line)
lightToTemperature, line = getSublist("light-to-temperature map:", txt, line)
temperatureToHumidity, line = getSublist("temperature-to-humidity map:", txt, line)
humidityToLocation, line = getSublist("humidity-to-location map:", txt, line)

# Convert setp by step

loc = seeds.copy()
loc = convert(loc, seedsToSoil)
loc = convert(loc, soilToFertilizer)
loc = convert(loc, fertilizerToWater)
loc = convert(loc, waterToLight)
loc = convert(loc, lightToTemperature)
loc = convert(loc, temperatureToHumidity)
loc = convert(loc, humidityToLocation)

print("The lowest location number is:", min(loc))






