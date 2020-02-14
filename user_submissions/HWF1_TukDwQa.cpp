#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    cout << "PROGRAM RUNNING";
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    fout << "Hello, World!";
    string s;
    fin >> s;
    fout << s;
    cout << s;
    cout << "PROGRAM END";

    return 0;
}
