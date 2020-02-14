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
    string s;
    fin >> s;
    if (s == "1" || s == "2" || s == "3")
    {
        fout << s;
    }

    return 0;
}
