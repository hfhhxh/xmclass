#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//#include <Windows.h>
#include <WinSock2.h>

#pragma comment(lib,"ws2_32.lib")

typedef struct _OVERLAPPEDExt{
	OVERLAPPED ol;
}OVERLAPPEDExt, *LPOVERLAPPEDExt;

DWORD WINAPI serverThreadProc(LPVOID lpParameter){
	HANDLE hCompletePort = HANDLE(lpParameter);
	srand(time(NULL));
	int id = rand() % 97;
	printf("I am thread %d.\n", id);
	//while (true){
	//	Sleep(100);
	//}
	DWORD trans;
	ULONG key;
	LPOVERLAPPED ol;
//	OVERLAPPED ol;
	::GetQueuedCompletionStatus(hCompletePort, &trans, &key, &ol, INFINITE);
	printf("I am thread %d. I get key %lu.\n", id, key);
	return 0;
}

int main(){
	printf("%d%d\n", sizeof(OVERLAPPED), sizeof(OVERLAPPEDExt));
	printf("%d%d%d\n", sizeof(ULONG), sizeof(DWORD), sizeof(HANDLE));
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);

	
	HANDLE hCompletePort = ::CreateIoCompletionPort(INVALID_HANDLE_VALUE, 0, 0, 0);
	DWORD threadId[6];
	HANDLE threadHd[6];
	for (int i = 0; i < 6; ++i){
		threadHd[i] = ::CreateThread(NULL, 0, serverThreadProc, (LPVOID)hCompletePort, 0, &threadId[i]);
		Sleep(1000);
	}
	Sleep(10000);
	for (int i = 0; i < 6; ++i){
		::PostQueuedCompletionStatus(hCompletePort, 0, i, 0);
	}
	for (int i = 0; i < 6; ++i){
		WaitForSingleObject(threadHd[i], INFINITE);
	}
	printf("END\n");
	getchar();

	WSACleanup();
	return 0;
}