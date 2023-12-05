#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

enum {STRING_LENGTH = 100};

const char textNumbers[10][10] = { 
    { "zero" }, { "one" }, { "two" } , { "three" }, { "four" },
    { "five" }, { "six" }, { "seven" }, { "eight" }, { "nine" }
};

// Search the last occurence of needle in haystack
char *strrstr(char *haystack, const char *needle)
{
    size_t needlen = strlen(needle);
    size_t h = strlen(haystack);
    size_t n = needlen;
    
    //checking every char, reverse
    while (h > 0)
    {
        //to restore the h value if the str is incomplete
        size_t prev_h = h;
        while((h > 0) && (n > 0) && (haystack[h - 1] == needle[n - 1]))
        {
            if(n == 1)
                return(haystack + h - 1);
            h--; n--;
        }
        h = prev_h - 1;
        n = needlen;
    }
    
    return NULL;
}

bool giveNumericNumbers(char *ln, char *first, char *last, int *fnp, int *lnp)
{
    bool found_first = false;
    for(int i = 0; i < strlen(ln); i++)
    {
        if(ln[i] >= '0' && ln[i] <= '9')
        {
            if(!found_first)
            {
                found_first = true;
                *first = ln[i];
                *fnp = i;
            }
            
            *last = ln[i];
            *lnp = i;
        }
    }
    return found_first;
}

bool giveTextNumbers(char *ln, char *first, char *last, int *ftp, int *ltp)
{
    bool found_first = false, found_last = false;
    *ftp = 0; *ltp = 0;
    
    for(int i = 0; i < 10; i++)
    {
        char *sub = strstr(ln, textNumbers[i]);
        if(NULL != sub)
        {
            int delta = sub - ln;
            if(delta < *ftp || !found_first)
            {
                *ftp = delta;
                *first = '0' + i;
                found_first = true;
            }
        }
        
        sub = strrstr(ln, textNumbers[i]);
        if(NULL != sub)
        {
            int delta = sub - ln;
            if(delta > *ltp || !found_last)
            {
                *ltp = delta;
                *last = '0' + i;
                found_last = true;
            }
        }
    }

    return found_first;
}

int main(int argc, char **argv)
{
    FILE *inputf = fopen("input.txt", "r");
    if(NULL == inputf)
    {
        perror("fopen: ");
        exit(EXIT_FAILURE);
    }
    
    char ln[STRING_LENGTH] = "";
    int sum = 0;
    
    while(NULL != fgets(ln, STRING_LENGTH, inputf))
    {
        char f, l, firstNum, lastNum, firstTxt, lastTxt;
        int fnp, lnp, ftp, ltp; //positions
        bool numericVals, textVals;
        
        numericVals = giveNumericNumbers(ln, &firstNum, &lastNum, &fnp, &lnp);
        textVals = giveTextNumbers(ln, &firstTxt, &lastTxt, &ftp, &ltp);
        if(!numericVals)
        {
            firstNum = firstTxt; lastNum = lastTxt;
        }
        else if(!textVals)
        {
            firstTxt = firstNum; lastTxt = lastNum;
        }
        f = (fnp < ftp) ? firstNum : firstTxt;
        l = (lnp > ltp) ? lastNum : lastTxt;
        
        char numstr[3] = "";
        numstr[0] = f;
        numstr[1] = l;
        
        int num = atoi(numstr);
        sum += num;
    }
    
    printf("The total sum is: %i\n", sum);    
    
    fclose(inputf);

    return 0;
}
