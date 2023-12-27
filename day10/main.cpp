#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <array>
#include <algorithm>

enum tiles {
    SE = 'F',
    SW = '7',
    NW = 'J',
    NE = 'L',
    HOR = '-',
    VERT = '|',
    GND = '.'
};

enum directions {
    NORTH,
    SOUTH,
    EAST,
    WEST
};

// Checks if we can go to a direction depending only on the current tile we are
bool checkDir(int sx, int sy, std::vector<std::string> &doc, int dir)
{
    char curTile = doc[sy][sx];
    switch(dir)
    {
        case NORTH:
            if((curTile == '|' or    
                curTile == NW or
                curTile == NE or
                curTile == 'S') and
                sy != 0)
                return true;
            break;
        case SOUTH:
            if((curTile == '|' or    
                curTile == SW or
                curTile == SE or
                curTile == 'S') and
                sy != (int) doc.size() - 1)
                return true;
            break;
        case EAST:
            if((curTile == '-' or    
                curTile == SE or
                curTile == NE or
                curTile == 'S') and
                sx != (int) doc[sy].size() - 1)
                return true;
            break;
        case WEST:
            if((curTile == '-' or    
                curTile == SW or
                curTile == NW or
                curTile == 'S') and
                sx != 0)
                return true;
            break;
    }
    return false;
}

// Checks if a direction has a tile we can reach
bool checkDestTile(int &sx, int &sy, std::vector<std::string> &doc, int dir)
{
    int sxTmp { sx }, syTmp { sy };
    char dstTile;
    switch(dir)
    {
        case NORTH:
            syTmp--;
            dstTile = doc[syTmp][sxTmp];
            if( dstTile == '|' or    
                dstTile == SW or
                dstTile == SE or
                dstTile == 'S'    )
            {
                sy = syTmp;
                return true;
            }
            break;
        case SOUTH:
            syTmp++;
            dstTile = doc[syTmp][sxTmp];
            if( dstTile == '|' or    
                dstTile == NW or
                dstTile == NE or
                dstTile == 'S'    )
            {
                sy = syTmp;
                return true;
            }
            break;
        case EAST:
            sxTmp++;
            dstTile = doc[syTmp][sxTmp];
            if( dstTile == '-' or    
                dstTile == SW or
                dstTile == NW or
                dstTile == 'S'    )
            {
                sx = sxTmp;
                return true;
            }
            break;
        case WEST:
            sxTmp--;
            dstTile = doc[syTmp][sxTmp];
            if( dstTile == '-' or    
                dstTile == SE or
                dstTile == NE or
                dstTile == 'S'    )
            {
                sx = sxTmp;
                return true;
            }
            break;
    }
    return false;
}

bool replacebounds(int &x, int &y, std::vector<std::string> &doc)
{
    bool correct = true;
    if(x < 0)
    {
        x = 0;
        correct = false;
    }
    if(y < 0)
    {
        y = 0;
        correct = false;
    }
    if(x >= (int) doc[0].size())
    {
        x = doc[0].size() - 1;
        correct = false;
    }
    if(y >= (int) doc.size())
    {
        y = doc.size() - 1;
        correct = false;
    }
    return correct;
}

void replaceEnclosedDots(int sx, int sy, std::vector<std::string> &doc, int dir, int &nb, std::vector<std::array<int, 2>> &iPos, bool left)
{
    int sxleft { sx }, sxright { sx }, syleft { sy }, syright { sy };

    switch(dir)
    {
        case NORTH:
            sxleft--;
            sxright++;
            break;
        case SOUTH:
            sxleft++;
            sxright--;
            break;
        case EAST:
            syleft--;
            syright++;
            break;
        case WEST:
            syleft++;
            syright--;
            break;
    }
    
    replacebounds(sxleft, syleft, doc);
    replacebounds(sxright, syright, doc);
    
    if(left)
    {
        if(doc[syleft][sxleft] == '.')
        {
            nb++;
            doc[syleft][sxleft] = 'I';
            iPos.push_back({ syleft, sxleft });
        }
    }
    else
    {
        if(doc[syright][sxright] == '.')
        {
            nb++;
            doc[syright][sxright] = 'I';
            iPos.push_back({ syright, sxright });
        }
    }
}

bool searchPath(int &sx, int &sy, std::vector<std::string> &doc, int &nb, std::vector<std::array<int, 2>> &iPos, bool left)
{
    int dir;
    int prevX { sx }, prevY{ sy };
    for(dir = 0; dir < 4; dir++)
    {
        
        if(checkDir(sx, sy, doc, dir) and (checkDestTile(sx, sy, doc, dir)))
        {
            doc[prevY][prevX] = ' ';
            replaceEnclosedDots(sx, sy, doc, dir, nb, iPos, left);
            replaceEnclosedDots(prevX, prevY, doc, dir, nb, iPos, left);
            return true;
        }
    }
    doc[prevY][prevX] = ' ';
    return false;
}

// Used by completeEnclosed
void completeEnclosedPos(std::vector<std::string> &doc, int &nb, std::vector<std::array<int, 2>> &iPos, int ix, int iy, int i)
{
    int y { iPos[i][0] }, x { iPos[i][1] };
    if(ix == 0 and iy == 0)
        return;
    x += ix;
    y += iy;
    if(!replacebounds(x, y, doc))
        return;
    if(doc[y][x] != ' ' and doc[y][x] != 'I')
    {
        doc[y][x] = 'I';
        iPos.push_back({y, x});
        nb++;
    }
}

// Look around every 'I' tiles (enclosed tiles that have been
// counted during path search). If a '.' is found near an 'I', 
// counter is incremented and this new tile becomes 'I'.
void completeEnclosed(std::vector<std::string> &doc, int &nb, std::vector<std::array<int, 2>> &iPos)
{
    /*
     * Looks if '?' tiles are dots
     * 
     * *?* 
     * ?I?
     * *?*
     * 
     */
    
    
    for(int i = 0; i < (int) iPos.size(); i++)
    {
        completeEnclosedPos(doc, nb, iPos, -1,  0, i);
        completeEnclosedPos(doc, nb, iPos,  1,  0, i);
        completeEnclosedPos(doc, nb, iPos,  0, -1, i);
        completeEnclosedPos(doc, nb, iPos,  0,  1, i);
    }
}

int main(void)
{
    std::ifstream in { "input.txt" };
    std::string s; // single line
    std::vector<std::string> doc, refl, refr; 
    // List of positions of enclosed tiles
    std::vector<std::array<int, 2>> iPosl, iPosr;
    
    if(!in.is_open())
    {
        std::cout << "Failed to open file.\n";
        return(1);
    }
    
    // Read file and search 'S' position
    int sxInit { 0 }, syInit { 0 };
    int i = 0;
    while(std::getline(in, s) and s != "")
    {
        doc.push_back(s);
        auto const fnd { std::find(std::begin(s), std::end(s), 'S') };
        if(fnd != std::end(s))
        {
            syInit = i;
            sxInit = fnd - std::begin(s);
        }
        i++;
    }
    
    std::copy(std::begin(doc), std::end(doc), std::back_inserter(refl));
    
    i = 0;
    int sx { sxInit }, sy { syInit };
    int nbl { 0 }, nbr { 0 };
    // Initial search
    // here, iPosl contains incorrect values
    while(searchPath(sx, sy, doc, nbl, iPosl, true))
        i++;
    i++;
    
    // Delete every pipes that are not in the path
    for(int j = 0; j < (int) doc.size(); j++)
    {
        for(int k = 0; k < (int) doc[j].size(); k++)
        {
            if(doc[j][k] != ' ')
                refl[j][k] = '.';
        }
    }
    
    // Does another research of path to count the enclosed tiles
    // Two counts will be done: one looking to the left, one looking to the right
    // refl and refr are like the initial grid, but all pipes that are not in
    // the path are replaced by '.'
    
    std::copy(std::begin(refl), std::end(refl), std::back_inserter(refr));
    
    // clear because incorrect values
    iPosl.clear();
    
    i = 0;
    int sxl { sxInit }, syl { syInit };
    int sxr { sxInit }, syr { syInit };
    nbl = 0;
    nbr = 0;
    while(searchPath(sxl, syl, refl, nbl, iPosl, true))
    {
        searchPath(sxr, syr, refr, nbr, iPosr, false);
        i++;
    }
    
    i++;
    
    std::cout << "Path size : " << i << std::endl;
    std::cout << "\nPART 1: farthest point : " << i / 2 << "\n";
    
    // Look around every 'I' tiles (enclosed tiles that have been
    // counted during path search). If a '.' is found near an 'I', 
    // counter is incremented and this new tile becomes 'I'.
    completeEnclosed(refl, nbl, iPosl);
    completeEnclosed(refr, nbr, iPosr);

    std::cout << "\nNumber of enclosed tiles (looking to the left): " << nbl << "\n";
    std::cout << "Number of enclosed tiles (looking to the right): " << nbr << "\n";
    
    // Keeps the lowest value, because the number of enclosed tiles is probably lower
    // than the number of tiles outside the loop. If the final answer isn't correct,
    // maybe the other answer should be tried.
    std::cout << "\nPART 2: the answer is (probably): ";
    if(nbl < nbr)
        std::cout << nbl << "\n";
    else 
        std::cout << nbr << "\n";
    
    return 0;
}
