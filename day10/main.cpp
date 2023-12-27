#include <iostream>
#include <fstream>
#include <string>
#include <vector>
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

bool searchPath(int &sx, int &sy, std::vector<std::string> &doc)
{
    int dir;
    for(dir = 0; dir < 4; dir++)
    {
        int prevX { sx }, prevY{ sy };
        if(checkDir(sx, sy, doc, dir) and (checkDestTile(sx, sy, doc, dir)))
        {
            doc[prevY][prevX] = '.';
//            std::cout << doc[prevY] << std::endl;
            return true;
        }
    }
    return false;
}

int main(void)
{
    std::ifstream in { "input.txt" };
    std::string s; // single line
    std::vector<std::string> doc; 
    
    if(!in.is_open())
    {
        std::cout << "Failed to open file.\n";
        return(1);
    }
    
    int sxInit { 0 }, syInit { 0 };
    int i = 0;
    while(std::getline(in, s) and s != "")
    {
//        std::cout << s << std::endl;;
        doc.push_back(s);
        // search 's'
        auto const fnd { std::find(std::begin(s), std::end(s), 'S') };
        if(fnd != std::end(s))
        {
            syInit = i;
            sxInit = fnd - std::begin(s);
        }
        i++;
    }
    
//    std::cout << sxInit << " " << syInit << std::endl;
    
    i = 0;
    int sx { sxInit }, sy { syInit };
    while(searchPath(sx, sy, doc))
    {
        i++;
        
//        for(auto const &e : doc)
//        {
//            std::cout << e << std::endl;
//        }
//        std::cout << std::endl << std::endl;
    }
    
    i++;
    
    std::cout << "path size : " << i << std::endl;
    std::cout << "farthest point : " << i / 2 << "\n";
    
    return 0;
}
