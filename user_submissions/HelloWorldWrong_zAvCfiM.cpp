#include <fstream>

using namespace std;

int main()
{
    ofstream fout("output.txt");
    fout << "Hello World!"; // Should be
    // fout << "Hello, World!"

    return 0;
}
