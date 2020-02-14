#include <fstream>

using namespace std;

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");

    int n;
    fin >> n;

    for (int i = 1; i <= n; i++)
    {
        if (i % 15 == 0)
            fout << "FizzBuzz ";
        else if (i % 3 == 0)
            fout << "Fizz ";
        else if (i % 5 == 0)
            fout << "Buzz ";
        else
            fout << i << " ";
    }

    return 0;
}
