#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include <cassert>
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
            case '9':
                tmp[i] = 8;
                break;
            case '8':
                tmp[i] = 7;
                break;
            case '7':
                tmp[i] = 6;
                break;
            case '6':
                tmp[i] = 5;
                break;
            case '5':
                tmp[i] = 4;
                break;
            case '4':
                tmp[i] = 3;
                break;
            case '3':
                tmp[i] = 2;
                break;
            case '2':
                tmp[i] = 1;
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

void splitInTypes
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

int sortTypes(std::array<std::vector<std::vector<int>>, 7> &types)
{
    auto compare = [](const std::vector<int> &a, const std::vector<int> &b)
    {
        return a.back() < b.back();
    };
    
    int cnt = 1;
    int add = 0;
    for(int i = 0; i < 7; i++)
    {
        std::sort(types[i].begin(), types[i].end(), compare);
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

int main()
{
    std::ifstream in { "input.txt" };
    std::string s;
    std::vector<std::vector<int>> vec;
    
    // 0 : high card -> 6 : five of a kind
    std::array<std::vector<std::vector<int>>, 7> types;
    
    // Generate a number representing the hand, each card is represented
    // by a number from 1 to 13.
    // { card1, card2, card3, card4, card5, bid, calculated_num }
    while (std::getline(in, s) and s != "")
    {
        std::vector<int> tmp = {0, 0, 0, 0, 0, 0, 0};
        parseline(tmp, s);        
        int num { 0 };
        for(int i=0; i<5; i++)
        {
            num += tmp[i] * pow(13., 5. - i);
        }
        tmp[6] = num;
        vec.push_back(tmp);
    }

    splitInTypes(vec, types);
    std::cout << "Part 1: the result is " << sortTypes(types) << std::endl;
   
    return 0;
}
