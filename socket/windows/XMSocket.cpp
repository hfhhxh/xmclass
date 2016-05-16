#include "XMSocket.h"
#include <string.h>
#include <stdio.h>

XMSocket::XMSocket(void): isServer(false), isTCP(false){
}

XMSocket::~XMSocket(void) {
	::closesocket(this->sock);
}

bool XMSocket::createServer(unsigned short port, bool isTCP) {
	this->isServer = true;
	this->isTCP = isTCP;
	int ret;
	if (this->isTCP) {
		sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (INVALID_SOCKET == sock) {
			return false;
		}
		memset(&addr, 0, sizeof(sockaddr_in));
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);
		addr.sin_addr.S_un.S_addr = INADDR_ANY;
		ret = bind(sock, (sockaddr*)&addr, sizeof(sockaddr));
		if (SOCKET_ERROR == ret) {
			return false;
		}
		ret = listen(sock, SOMAXCONN);
		if (SOCKET_ERROR == ret) {
			return false;
		}
	} else {
		sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		if (INVALID_SOCKET == sock) {
			return false;
		}
		memset(&addr, 0, sizeof(sockaddr_in));
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);
		addr.sin_addr.S_un.S_addr = INADDR_ANY;
		ret = bind(sock, (sockaddr*)&addr, sizeof(sockaddr));
		if (SOCKET_ERROR == ret) {
			return false;
		}
	}
	return true;
}

bool XMSocket::createClient(unsigned short port, const char * ip, bool isTCP) {
	this->isServer = false;
	this->isTCP = isTCP;
	if (this->isTCP) {
		sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (INVALID_SOCKET == sock) {
			return false;
		}
		memset(&addr, 0, sizeof(sockaddr_in));
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);
		addr.sin_addr.S_un.S_addr = inet_addr(ip);
	} else {
		sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		if (INVALID_SOCKET == sock) {
			return false;
		}
		memset(&addr, 0, sizeof(sockaddr_in));
		addr.sin_family = AF_INET;
		addr.sin_port = htons(port);
		addr.sin_addr.S_un.S_addr = inet_addr(ip);
	}
	return true;
}

bool XMSocket::accept(XMSocket & client) {
	int sin_size = sizeof(sockaddr);
	client.sock = ::accept(this->sock, (sockaddr*)&client.addr, &sin_size);
	if(INVALID_SOCKET == client.sock){
		return false;
	}
	return true;
}

bool XMSocket::connect() {
	int ret = ::connect(this->sock, (sockaddr*)&this->addr, sizeof(sockaddr));
	if(SOCKET_ERROR == ret){
		return false;
	}
	return true;
}

int XMSocket::send(const char * buf, int len) {
	if (isTCP) {
		return ::send(this->sock, buf, len, 0);
	} else {
		int sin_size = sizeof(sockaddr);
		return ::sendto(this->sock, buf, len, 0, (sockaddr *)&this->addr, sin_size);
	}
}

int XMSocket::recv(char * buf, int len) {
	memset(buf, 0, len);
	if (isTCP) {
		return ::recv(this->sock, buf, len, 0);
	} else {
		int sin_size = sizeof(sockaddr);
		return ::recvfrom(this->sock, buf, len, 0, (sockaddr *)&this->addr, &sin_size);
	}
}

int XMSocket::send(const sockaddr_in & client, const char * buf, int len) {
	int sin_size = sizeof(sockaddr);
	return ::sendto(this->sock, buf, len, 0, (sockaddr *)&client, sin_size);
}

int XMSocket::recv(sockaddr_in & client, char * buf, int len) {
	memset(buf, 0, len);
	int sin_size = sizeof(sockaddr);
	return ::recvfrom(this->sock, buf, len, 0, (sockaddr *)&client, &sin_size);
}

void XMSocket::close() {
	::closesocket(this->sock);
}

void XMSocket::startup() {
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);
}

void XMSocket::cleanup() {
	WSACleanup();
}

void XMSocket::setaddr(sockaddr_in & addr, unsigned short port, const char * ip) {
	memset(&addr, 0, sizeof(sockaddr_in));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	if (NULL == ip) {
		addr.sin_addr.S_un.S_addr = INADDR_ANY;
	} else {
		addr.sin_addr.S_un.S_addr = inet_addr(ip);
	}
}

bool XMSocket::setbloking(bool block){
	unsigned long ul = (block ? 0 : 1);
	return 0 == ::ioctlsocket(this->sock, FIONBIO, (unsigned long *)&ul);
}