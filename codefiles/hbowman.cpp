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
    char s;
    fin >> s;
    fout << s;

    return 0;
}
