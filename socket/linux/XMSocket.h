#ifndef ___XMSOCKET_H___
#define ___XMSOCKET_H___

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

class XMSocket {
private:
  bool isServer;
  bool isTCP;
  int fd;
  sockaddr_in addr;
public:
  XMSocket(void);
//    XMSocket(int fd);
  virtual ~XMSocket();

  bool createServer(unsigned short port, bool isTCP = true);
  bool createClient(unsigned short port, const char *ip, bool isTCP = true);
  bool accept(XMSocket & client);
  bool connect();
  int send(const char* buf, int len);
  int recv(char *buf, int len);
  int send(sockaddr_in & client, const char * buf, int len);
  int recv(sockaddr_in & client, char * buf, int len);
  void close();
	bool setbloking(bool block);
//    int fd();
//    bool create();
//    bool bind(short port);
//    bool listen(int backlog=128);
//    bool accept(XMSocket &client, sockaddr_in *sa=NULL, int *len=NULL);
//    bool connect(char *ip, short port);
//    int send(char *buf, int size, int flag=0);
//    int recv(char *buf, int size, int flag=0);
//    bool close();
//    int getsockname(sockaddr_in *sa);
//    int getpeername(sockaddr_in *sa);
//    int setnonblocking();
};

#endif /* ___XMSOCKET_H___ */
