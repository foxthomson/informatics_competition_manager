#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    fout << "Hello, World!";
    string s;
    fin >> s;
    fout << s;
    cout << s;

    return 0;
}
