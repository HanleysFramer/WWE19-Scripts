#include <Windows.h>
#include <iostream>
#include <vector>
#include <TlHelp32.h>
#include <tchar.h>
#include <fstream>
#include <string>

using namespace std;


DWORD64 dwGetModuleBaseAddress(TCHAR *lpszModuleName, DWORD pID) {
	DWORD64 dwModuleBaseAddress = 0;
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pID);
	MODULEENTRY32 ModuleEntry32 = { 0 };
	ModuleEntry32.dwSize = sizeof(MODULEENTRY32);

	if (Module32First(hSnapshot, &ModuleEntry32))
	{
		do {
			if (_tcscmp(ModuleEntry32.szModule, lpszModuleName) == 0)
			{
				dwModuleBaseAddress = (DWORD64)ModuleEntry32.modBaseAddr;
				break;
			}
		} while (Module32Next(hSnapshot, &ModuleEntry32));


	}
	CloseHandle(hSnapshot);
	return dwModuleBaseAddress;
}


int main() {

	DWORD pID;
	char moduleName[] = "WWE2K19_x64.exe";
	HWND hGameWindow;
	HANDLE pHandle;

	//Get Handles
	hGameWindow = FindWindow(NULL, "WWE 2K19");
	GetWindowThreadProcessId(hGameWindow, &pID);
	pHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pID);

	//*debug cout << "PID: " << pID << '\n';

	for (int i = 1; i < 7; i = i + 1)

	{
		//*debug counts loop
		//cout << i << '\n';

		DWORD off1;
		DWORD64 off2;
		DWORD baseAddress;
		char chunk_mem[900000];

		int len_mem = 1;

			if (i > 1)
			{
				int a = ((i - 1) * 900000);
				SIZE_T bytesRead;

				//Get Base Address
				DWORD64 clientBase = dwGetModuleBaseAddress(_T(moduleName), pID);
				ReadProcessMemory(pHandle, (LPCVOID)(clientBase + 0x025ECBC8), &baseAddress, sizeof(baseAddress), NULL);   // BasePointer
				ReadProcessMemory(pHandle, (LPCVOID)(baseAddress + 0x88), &off1, sizeof(off1), NULL);                      // Pointer Offset 1 or Chunk Start
				ReadProcessMemory(pHandle, (LPCVOID)(off1), &off2, sizeof(off2), NULL);
				ReadProcessMemory(pHandle, (LPCVOID)((off1 + a)- 8), chunk_mem, sizeof(chunk_mem), NULL);

				if (baseAddress < 10){
					cout << "Chunk capture failed. Please restart 'WWE 2k19' and try again.";
					cout << '\n';
					system("pause");
					return 0;
				}

				//*debug cout << "Chunk_Start: " << std::hex << off1 << '\n';

				//outputs to file
				ofstream myfile2;
				myfile2.open("chunk_extract.bin", ios_base::binary | ios_base::out | ios_base::app);
				myfile2.write((char*)&chunk_mem, sizeof(chunk_mem));
				myfile2.close();
			}

			else
			{
				int a = (900000);
				SIZE_T bytesRead;

				//Get Base Address
				DWORD64 clientBase = dwGetModuleBaseAddress(_T(moduleName), pID);
				ReadProcessMemory(pHandle, (LPCVOID)(clientBase + 0x025ECBC8), &baseAddress, sizeof(baseAddress), NULL);   // BasePointer
				ReadProcessMemory(pHandle, (LPCVOID)(baseAddress + 0x88), &off1, sizeof(off1), NULL);                      // Pointer Offset 1 or Chunk Start
				ReadProcessMemory(pHandle, (LPCVOID)(off1), &off2, sizeof(off2), NULL);
				ReadProcessMemory(pHandle, (LPCVOID)(off1 - 8), chunk_mem, sizeof(chunk_mem), NULL);

				if (baseAddress < 10) {
					cout << "Chunk capture failed. Please restart 'WWE 2k19' and try again.";
					cout << '\n';
					system("pause");
					return 0;
				}

				//*debug cout << "Chunk_Start: " << std::hex << off1 << '\n';

				//outputs to file
				ofstream myfile2;
				myfile2.open("chunk_extract.bin", ios_base::binary | ios_base::out | ios_base::app);
				myfile2.write((char*)&chunk_mem, sizeof(chunk_mem));
				myfile2.close();
			}
	}

	cout << "Chunk capture successful. Press any key to exit. \n";
	cout << '\n';
	system("pause");
	cin.clear();
}
