#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include <limits>

enum { HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, FULL_HOUSE,
       FOUR_OF_A_KIND, FIVE_OF_A_KIND };

void parseline(std::vector<int> &tmp, std::string s)
{
    for(int i = 0; i < 5; i++)
    {
        switch(s[i])
        {
            case 'A':
                tmp[i] = 13;
                break;
            case 'K':
                tmp[i] = 12;
                break;
            case 'Q':
                tmp[i] = 11;
                break;
            case 'J':
                tmp[i] = 10;
                break;
            case 'T':
                tmp[i] = 9;
                break;
            default:
                tmp[i] = std::stoi(s.substr(i, 1)) - 1;
                break;
        }
    }
        
    s = s.substr(6);
    tmp[5] = std::stoi(s);
}

void findtimes(std::vector<int> e, std::array<int, 13> &times)
{
    times.fill(0);
    
    for(int j = 0; j < 5; j++)
    {
        if(times[e[j] - 1] != 0)
            continue;
        times[e[j] - 1]++;
        for(int k = 0; k < 5; k++)
        {
            if(j != k and e[j] == e[k])
                times[e[j] - 1]++;
        }
    }
}

void splitInTypesP1
(
    std::vector<std::vector<int>> vec, 
    std::array<std::vector<std::vector<int>>, 7> &types
)
{
    std::array<int, 13> times;

    // Type
    for(auto const &e : vec)
    {
        findtimes(e, times);
        
        std::array<int, 5> occurences;
        occurences.fill(0);
        for(auto const t : times)
        {
            if(t != 0)
                occurences[t-1]++;
        }
        
        // split occurences
        if(occurences[4] == 1)
            types[FIVE_OF_A_KIND].push_back(e);
        else if(occurences[3] == 1)
            types[FOUR_OF_A_KIND].push_back(e);
        else if(occurences[2] == 1 and occurences[1] == 1)
            types[FULL_HOUSE].push_back(e);
        else if(occurences[2] == 1)
            types[THREE_OF_A_KIND].push_back(e);
        else if(occurences[1] == 2)
            types[TWO_PAIR].push_back(e);
        else if(occurences[1] == 1)
            types[ONE_PAIR].push_back(e);
        else
            types[HIGH_CARD].push_back(e);
    }
}

void splitInTypesP2
(
    std::vector<std::vector<int>> vec, 
    std::array<std::vector<std::vector<int>>, 7> &types
)
{
    std::array<int, 13> times;

    // Type
    for(auto const &e : vec)
    {
        findtimes(e, times);
        
        int nbJoker { 0 };
        std::array<int, 5> occurences;
        occurences.fill(0);
        int i { 0 }, max { 0 };
        for(auto const t : times)
        {
            if(i == 9)
            {
                nbJoker = t;
                times[i] = 0;
            }
            else if(t != 0)
            {
                occurences[t-1]++;
                max = (t > max) ? t : max;
            }

            i++;
        }
        
        occurences[max + nbJoker - 1]++;
        occurences[max - 1]--;
        
        // split occurences
        if(occurences[4] == 1)
            types[FIVE_OF_A_KIND].push_back(e);
        else if(occurences[3] == 1)
            types[FOUR_OF_A_KIND].push_back(e);
        else if(occurences[2] == 1 and occurences[1] == 1)
            types[FULL_HOUSE].push_back(e);
        else if(occurences[2] == 1)
            types[THREE_OF_A_KIND].push_back(e);
        else if(occurences[1] == 2)
            types[TWO_PAIR].push_back(e);
        else if(occurences[1] == 1)
            types[ONE_PAIR].push_back(e);
        else
            types[HIGH_CARD].push_back(e);
    }
}

int sortTypes(std::array<std::vector<std::vector<int>>, 7> &types, bool p2)
{
    auto compareP1 = [](const std::vector<int> &a, const std::vector<int> &b)
    {
        return a[6] < b[6];
    };
    
    auto compareP2 = [](const std::vector<int> &a, const std::vector<int> &b)
    {
        return a[7] < b[7];
    };
    
    int cnt = 1;
    int add = 0;
    for(int i = 0; i < 7; i++)
    {
        if(!p2)
            std::sort(types[i].begin(), types[i].end(), compareP1);
        else
            std::sort(types[i].begin(), types[i].end(), compareP2);
        for(const auto &e : types[i])
        {
            add += e[5] * cnt;
            cnt++;
        } 
    }
    return add;
}

int sum(std::array<std::vector<std::vector<int>>, 7> &types)
{
    int i = 1;
    int add = 0;
    for(auto const &e : types)
    {
        for(auto const &f : e)
        {
            add += f[5] * i;
            i++;
        }
    }
    return add;
}

void part1(std::vector<std::vector<int>> vec)
{
    // first dim
    // 0 : high card -> 6 : five of a kind
    std::array<std::vector<std::vector<int>>, 7> types;
    
    splitInTypesP1(vec, types);
    std::cout << "Part 1: the result is " << sortTypes(types, false) << std::endl;
}

void part2(std::vector<std::vector<int>> vec)
{
    // first dim
    // 0 : high card -> 6 : five of a kind
    std::array<std::vector<std::vector<int>>, 7> types;
    
    splitInTypesP2(vec, types);
    std::cout << "Part 2: the result is " << sortTypes(types, true) << std::endl;
}

int main()
{
    std::ifstream in { "input.txt" };
    std::string s;
    std::vector<std::vector<int>> vec;

    
    // Generate a number representing the hand, each card is represented
    // by a number from 1 to 13 (for part 1)
    // For part 2, a J is represented by a 0.
    // The number is then calculated with a power of 14. It allows to sort
    // hands.
    // { card1, card2, card3, card4, card5, bid, calc_num_part1, calc_num_part2 }
    while (std::getline(in, s) and s != "")
    {
        std::vector<int> tmp = {0, 0, 0, 0, 0, 0, 0, 0};
        parseline(tmp, s);        
        int num { 0 }, num2 { 0 };
        if(tmp[5] == 187 or tmp[5] == 633)
        {
            
        }
        for(int i=0; i<5; i++)
        {
            double add { tmp[i] * pow(14., 4. - i) };
            num += add;
            if(tmp[i] != 10) // if not J
                num2 += add;
        }
        tmp[6] = num;
        tmp[7] = num2;
        vec.push_back(tmp);
    }

    part1(vec);
    part2(vec);
   
    return 0;
}
