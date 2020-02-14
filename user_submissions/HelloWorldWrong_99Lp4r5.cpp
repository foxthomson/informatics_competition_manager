#include <fstream>

using namespace std;

int main()
{
    ofstream fout("output.txt");
    fout << "Hello World!"; // Should be
    // fout << "Hello, World!"

    retrun 0; // syntax error on this line
    // should be return 0;
}
