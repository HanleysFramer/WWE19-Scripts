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
