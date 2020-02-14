#include <iostream>
#include <windows.h>
#include <string>
#include <fstream>
#include <cstdlib>

using namespace std;

string ExePath() {
    char buffer[MAX_PATH];
    GetModuleFileName( NULL, buffer, MAX_PATH );
    string::size_type pos = string( buffer ).find_last_of( "\\/" );
    return string( buffer ).substr( 0, pos);
}

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    std::string s((std::istreambuf_iterator<char>(t)),
                     std::istreambuf_iterator<char>());
    fout << s;

    system("ls");

    return 0;
}
