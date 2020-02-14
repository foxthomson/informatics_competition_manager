/*
ID: 11athom1
PROG: nocows
LANG: C++
*/

#include <iostream>
#include <fstream>

using namespace std;

int n, k;

int workingpos[200];
int notworkingpos[200];

void getpos(int height)
{
    if (height == 2)
    {
        // base case - setup arrays
        workingpos[3] = 1;
        notworkingpos[1] = 1;
    }
    else
    {
        getpos(height - 1);

        // cout << endl << endl << height << endl;
        // for (int i = 0; i < 200; i++)
        // {
        //     cout << workingpos[i] << "\t" << notworkingpos[i] << endl;
        // }

        // create new arrays to be copied over when finished
        int newworkingpos[200];
        int newnotworkingpos[200];
        for (int i = 0; i < 200; i++)
        {
            newworkingpos[i] = 0;
            newnotworkingpos[i] = 0;
        }

        // add

        for (int i = 1; i < 200; i+=2)
        {
            // cout << i << workingpos[i] << notworkingpos[i] << endl;
            // can finish if reached the zeros in the array
            if ((workingpos[i] == 0) && (notworkingpos[i] == 0))
            {
                break;
            }

            for (int j = 1; j < 200; j+=2)
            {
                // can finish if reached the zeros in the array
                if ((workingpos[j] == 0) && (notworkingpos[j] == 0))
                {
                    break;
                }

                // can finish if sums greater than 200
                if (i + j + 1 > 200)
                {
                    break;
                }

                // add to new
                // cout << i << j << workingpos[i] << workingpos[j] << notworkingpos[i] << notworkingpos[j] << endl;
                // cout << i << " " << j << endl;

                newworkingpos[i + j + 1] += (workingpos[i] * workingpos[j]) % 9901;
                newworkingpos[i + j + 1] += (workingpos[i] * notworkingpos[j]) % 9901;
                newworkingpos[i + j + 1] += (notworkingpos[i] * workingpos[j]) % 9901;
                newnotworkingpos[i + j + 1] += (notworkingpos[i] * notworkingpos[j]) % 9901;
                newworkingpos[i + j + 1] %= 9901;
                newnotworkingpos[i + j + 1] %= 9901;
            }
        }

        // copy array
        for (int i = 0; i <200; i++)
        {
            workingpos[i] = newworkingpos[i];
            notworkingpos[i] = newnotworkingpos[i];
            // cout << workingpos[i] << "\t" << notworkingpos[i] << endl;
        }

        // add 1
        notworkingpos[1] = 1;

        // cout << endl << endl << height << endl;
        // for (int i = 0; i < 200; i++)
        // {
        //     cout << workingpos[i] << "\t" << notworkingpos[i] << endl;
        // }
    }
}

int main()
{
    ifstream fin("nocows.in");
    ofstream fout("nocows.out");

    // input
    fin >> n >> k;

    getpos(k);

    // output
    fout << workingpos[n] << endl;
    cout << workingpos[n] << endl;

    return 0;
}
