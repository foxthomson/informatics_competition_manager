#include <iostream>
#include <windows.h>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

int mainm()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    string s;
    fin >> s;
    fout << s;

    return 0;
}
