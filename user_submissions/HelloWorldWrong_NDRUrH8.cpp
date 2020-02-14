#include <fstream>

using namespace std;

int main()
{
    ofstream fout("output.txt");
    while (1) // infinte loop
        fout << "Hello, World!";

    return 0;
}
