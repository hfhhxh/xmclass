#include "ae.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <fcntl.h>
#include <errno.h>

extern int errno;

#define MAXFD 10280

char *str = "hello";

int nsend = 0, nrecv = 0;
pthread_mutex_t lsend, lrecv;

int setnonblock(int fd) {
	int flags = fcntl(fd, F_GETFL);
	flags |= O_NONBLOCK;
	return fcntl(fd, F_SETFL, flags);
}

void clientProc(struct aeEventLoop *eventLoop, int fd, void *clientData, int mask) {
	char *buf = (char *)malloc(1024*sizeof(char));
  if(NULL == buf) { puts("malloc error."); return; }
	int r = recv(fd, buf, 1024, 0);
	if(-1 == r) {
		if(-1 == r && errno != EAGAIN) {
      //printf("recv %s\n", strerror(errno)); 
			aeDeleteFileEvent(eventLoop, fd, mask);
			close(fd);
		}
	} else if (0 == r) {
		aeDeleteFileEvent(eventLoop, fd, mask);
		close(fd);
	} else if (5 == r){
		pthread_mutex_lock(&lrecv);
		++nrecv;
		pthread_mutex_unlock(&lrecv);
	  int s = send(fd, buf, r, 0);
		if(5 == s) {
      pthread_mutex_lock(&lsend);
      ++nsend;
      pthread_mutex_unlock(&lsend);
    } else {
			puts("send incomplote.");		
		}
	} else {
		puts("recv incomplote.");		
	}
//	printf("%d %d\n", nsend, nrecv);
	free(buf);
}

void serverProc(struct aeEventLoop *eventLoop, int fd, void *clientData, int mask) {
	int clnt_sock = accept(fd, NULL, NULL);
	if(-1 == clnt_sock) { printf("accept %s\n", strerror(errno)); return; }
	setnonblock(clnt_sock);
	aeCreateFileEvent(eventLoop, clnt_sock, AE_READABLE, clientProc, NULL);
}

int main(int argc, char **argv) {
	int port = atoi(argv[1]);	
  
	int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	struct sockaddr_in serv_addr;	
	memset(&serv_addr, 0, sizeof(serv_addr));  //每个字节都用0填充
	serv_addr.sin_family = AF_INET;  //使用IPv4地址
	serv_addr.sin_addr.s_addr = INADDR_ANY;  //具体的IP地址
	serv_addr.sin_port = htons(port);  //端口
	bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
	listen(serv_sock, MAXFD);
	setnonblock(serv_sock);
  
	pthread_mutex_init(&lsend, NULL);
	pthread_mutex_init(&lrecv, NULL);
  
	aeEventLoop *eventLoop = aeCreateEventLoop(MAXFD);
	aeCreateFileEvent(eventLoop, serv_sock, AE_READABLE, serverProc, NULL);
  aeMain(eventLoop);
  
	return 0;
}
