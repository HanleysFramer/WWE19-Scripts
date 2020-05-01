// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <string>
#include <Windows.h>
using namespace std;

DWORD pid;
DWORD Ammo = 0x0A994DF0;
string MyAmmo;

int main()
{
	HWND hWnd = FindWindowA(0, ("WWE 2K19"));

	GetWindowThreadProcessId(hWnd, &pid);
	HANDLE pHandle = OpenProcess(PROCESS_VM_READ, FALSE, pid);
	ReadProccessMemory(pHandle, (LPVOID)Ammo, &MyAmmo, sizeof(MyAmmo), 0);
	cout << MyAmmo << endl;
	system("Pause");
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu
