#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    ofstream fout("output.txt");
    fout << "Hello, World!";

    return 0;
}
