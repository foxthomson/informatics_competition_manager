#include <iostream>
#include <windows.h>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

int main()
{
    ifstream fin("inpu.txt");
    ofstream fout("output.txt");
    string s;
    fin >> s;
    fout << s;

    return 0;
}
