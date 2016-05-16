#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//#include <WinSock2.h>
#include "..\XMSocket\XMSocket.h"

#pragma comment(lib,"ws2_32.lib")

typedef struct _OVERLAPPEDExt{
	OVERLAPPED ol;
	char data[1024];
//	int lenth;
	int iotype;	//0, read, 1, write
}OVERLAPPEDExt, *LPOVERLAPPEDExt;

//typedef struct _SOCKADDR{
//	SOCKET sock;
//	sockaddr_in addr;
//}SOCKADDR, LPSOCKADDR;

DWORD WINAPI serverThreadProc(LPVOID lpParameter){
	puts("thread start.");
	HANDLE hCompletePort = HANDLE(lpParameter);
	DWORD trans;
	LPOVERLAPPEDExt lol = NULL;
	// = (LPOVERLAPPEDExt)malloc(sizeof(OVERLAPPEDExt))
	XMSocket *client = NULL;
	while (true){
		::GetQueuedCompletionStatus(hCompletePort, &trans, (PULONG_PTR)&client, (LPOVERLAPPED *)&lol, INFINITE);
//		puts("GetQueuedCompletionStatus");
		WSABUF buf;
		buf.buf = lol->data;
		DWORD dwFlag = 0;
		switch (lol->iotype){
		case 0:	//recv complete
			printf("recv %3d:%s\n", trans, lol->data);
			//			WSABUF buf;
			//			buf.buf = lol->data;			
			buf.len = trans;
			lol->iotype = 1;
			//		DWORD dwRecv = 0;
			//			DWORD dwFlag = 0;
			::WSASend(client->getsock(), &buf, 1, NULL, dwFlag, (LPOVERLAPPED)lol, NULL);
			break;
		case 1:	//send complete
			printf("send %3d:%s\n", trans, lol->data);
//			WSABUF buf;
//			buf.buf = lol->data;
			buf.len = 1024;
			lol->iotype = 0;
			//		DWORD dwRecv = 0;
//			DWORD dwFlag = 0;
			memset(lol->data, 0, sizeof(lol->data));
			::WSARecv(client->getsock(), &buf, 1, NULL, &dwFlag, (LPOVERLAPPED)lol, NULL);
			break;
		}
		
	}
	return 0;
}

int main(){
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);

	HANDLE hCompletePort = ::CreateIoCompletionPort(INVALID_HANDLE_VALUE, 0, 0, 0);
	DWORD threadId[6];
	HANDLE threadHd[6];
	for (int i = 0; i < 6; ++i){
		threadHd[i] = ::CreateThread(NULL, 0, serverThreadProc, (LPVOID)hCompletePort, 0, &threadId[i]);
//		Sleep(1000);
	}
	XMSocket server;
	server.createServer(8888);
	XMSocket *client;
	while (true){
		client = new XMSocket;
		server.accept(*client);
		::CreateIoCompletionPort((HANDLE)client->getsock(), hCompletePort, (DWORD)client, 0);
		LPOVERLAPPEDExt lol = (LPOVERLAPPEDExt)malloc(sizeof(OVERLAPPEDExt));
		memset(lol, 0, sizeof(OVERLAPPEDExt));
		WSABUF buf;
		buf.buf = lol->data;
		buf.len = 1024;
		lol->iotype = 0;
		//DWORD dwRecv = 0;
		DWORD dwFlag = 0;
//		DWORD trans = 0;
		int ret = ::WSARecv(client->getsock(), &buf, 1, NULL, &dwFlag, &lol->ol, NULL);
//		printf("%d\n%d\n", ret, trans);
	}
	
	//for (int i = 0; i < 6; ++i){
	//	::PostQueuedCompletionStatus(hCompletePort, 0, i, 0);
	//}

	//for (int i = 0; i < 6; ++i){
	//	WaitForSingleObject(threadHd[i], INFINITE);
	//}

	WSACleanup();

	printf("END\n");
	getchar();
	return 0;
}