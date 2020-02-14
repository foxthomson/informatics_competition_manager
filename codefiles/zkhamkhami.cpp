#include <iostream>
#include <windows.h>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    int s;
    fin >> s;
    while (s%3 == 0)
    {
        ;
    }
    fout << s;

    return 0;
}
