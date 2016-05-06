#ifndef ___XMSOCKET_H___
#define ___XMSOCKET_H___

#pragma once
#include <WinSock2.h>
#pragma comment(lib,"ws2_32.lib")

class XMSocket {
private:
	bool isServer;
	bool isTCP;
	SOCKET sock;
	sockaddr_in addr;
public:
	XMSocket(void);
	virtual ~XMSocket(void);

	bool createServer(unsigned short port, bool isTCP = true);
	bool createClient(unsigned short port, const char *ip, bool isTCP = true);
	bool accept(XMSocket & client);
	bool connect();
	int send(const char *buf, int len);
	int recv(char *buf, int len);
	int send(const sockaddr_in & client, const char *buf, int len);
	int recv(sockaddr_in & client, char *buf, int len);
	void close();
	static void startup();
	static void cleanup();
	static void setaddr(sockaddr_in & addr, unsigned short port, const char *ip = NULL);
	bool setbloking(bool block);
};

#endif 