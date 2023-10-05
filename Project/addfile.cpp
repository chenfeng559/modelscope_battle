#include <iostream>
#include <fstream>
#include <windows.h>
using namespace std;

int main(){
//	system("cd ./modelscope_battle");
	
	int i = 1;
	for(int i=0;i<500;i++){
		ofstream fout;  fout.open("./1.txt");
		fout<<i; fout.close();
		system("git add .");
		system("git commit 1.txt -m \'add\'");
		system("git push");
		Sleep(5);
	}
	return 0;
}
