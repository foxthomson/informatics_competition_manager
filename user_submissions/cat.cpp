#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    string s;
    fin >> s;
    fout << s;
    
    return 0;
}
