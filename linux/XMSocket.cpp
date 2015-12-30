#include "XMSocket.h"
#include <string.h>

XMSocket::XMSocket(void): isServer(false), isTCP(false){
}


XMSocket::~XMSocket(void){
    ::close(this->fd);
}

bool XMSocket::createServer(unsigned short port, bool isTCP){
    this->isServer = true;
    this->isTCP = isTCP;
    int ret;
    if (this->isTCP) {
        fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (-1 == fd) {
            return false;
        }
        memset(&addr, 0, sizeof(sockaddr_in));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = INADDR_ANY;
        ret = bind(fd, (sockaddr*)&addr, sizeof(sockaddr));
        if (-1 == ret) {
            return false;
        }
        ret = listen(fd, SOMAXCONN);
        if (-1 == ret) {
            return false;
        }
    } else {
        fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (-1 == fd) {
            return false;
        }
        memset(&addr, 0, sizeof(sockaddr_in));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = INADDR_ANY;
        ret = bind(fd, (sockaddr*)&addr, sizeof(sockaddr));
        if (-1 == ret) {
            return false;
        }
    }
    return true;
}

bool XMSocket::createClient(unsigned short port, const char *ip, bool isTCP){
    this->isServer = false;
    this->isTCP = isTCP;
    if (this->isTCP) {
        fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (-1 == fd) {
            return false;
        }
        memset(&addr, 0, sizeof(sockaddr_in));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr(ip);
    } else {
        fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (-1 == fd) {
            return false;
        }
        memset(&addr, 0, sizeof(sockaddr_in));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        addr.sin_addr.s_addr = inet_addr(ip);
    }
    return true;
}

bool XMSocket::accept(XMSocket & client){
    int sin_size = sizeof(sockaddr);
    client.fd = ::accept(this->fd, (sockaddr*)&client.addr, (socklen_t *)&sin_size);
    if(-1 == client.fd){
        return false;
    }
    return true;
}

bool XMSocket::connect(){
    int ret = ::connect(this->fd, (sockaddr*)&this->addr, sizeof(sockaddr));
    if(-1 == ret){
        return false;
    }
    return true;
}

int XMSocket::send(const char* buf, int len){
    if (isTCP) {
        return ::send(this->fd, buf, len, 0);
    } else {
        int sin_size = sizeof(sockaddr);
        return ::sendto(this->fd, buf, len, 0, (sockaddr *)&this->addr, sin_size);
    }
}

int XMSocket::recv(char *buf, int len){
    memset(buf, 0, len);
    if (isTCP) {
        return ::recv(this->fd, buf, len, 0);
    } else {
        int sin_size = sizeof(sockaddr);
        return ::recvfrom(this->fd, buf, len, 0, (sockaddr *)&this->addr, (socklen_t *)&sin_size);
    }
}

int XMSocket::send(sockaddr_in & client, const char * buf, int len){
    int sin_size = sizeof(sockaddr);
    return ::sendto(this->fd, buf, len, 0, (sockaddr *)&client, sin_size);
}

int XMSocket::recv(sockaddr_in &client, char * buf, int len){
    memset(buf, 0, len);
    int sin_size = sizeof(sockaddr);
    return ::recvfrom(this->fd, buf, len, 0, (sockaddr *)&client, (socklen_t *)&sin_size);
}

void XMSocket::close(){
    ::close(this->fd);
}
