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

char *ip;
int port, thdnum, reqnum;
char *str = "hello";

int nsend = 0, nrecv = 0;
pthread_mutex_t lsend, lrecv;

int setnonblock(int fd) {
  int flags = fcntl(fd, F_GETFL);
  flags |= O_NONBLOCK;
	return fcntl(fd, F_SETFL, flags);
}

void *clientProc(void *arg) {
  pthread_t *tid = (pthread_t *)arg;
//	printf("thread %d start.\n", d->id);
	int sock = socket(AF_INET, SOCK_STREAM, 0);
  if(-1 == sock) { puts("socket error."); exit(1); }
	struct sockaddr_in serv_addr;
  memset(&serv_addr, 0, sizeof(serv_addr));  //每个字节都用0填充
  serv_addr.sin_family = AF_INET;  //使用IPv4地址
  serv_addr.sin_addr.s_addr = inet_addr(ip);  //具体的IP地址
  serv_addr.sin_port = htons(port);  //端口
  int conn = connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
  if(-1 == conn) { puts("connect error."); printf("%s\n", strerror(errno));  return NULL; }
	
  int cnt = 0;
	char *buf = (char *)malloc(1024*sizeof(char));
  if(NULL == buf) { puts("malloc error."); close(sock); return NULL; }
	for(int i = 0; i < reqnum; ++i) {
		int s = send(sock, str, 5, 0);
		if(5 == s) {
			pthread_mutex_lock(&lsend);
      ++nsend;
      pthread_mutex_unlock(&lsend);
		} else {
			puts("send incomplote."); 
		}
		int r = recv(sock, buf, 1024, 0);
		if(-1 == r) {
			if(-1 == r && errno != EAGAIN) {
        //printf("recv %s\n", strerror(errno));
				close(sock);
				free(buf);
        printf("%d\n", cnt);
				return NULL;
			}
    } else if(0 == r) {
			close(sock);
			free(buf);
      printf("%d\n", cnt);
			return NULL;
		} else if(5 == r){
    	pthread_mutex_lock(&lrecv);
	    ++nrecv;
  	  pthread_mutex_unlock(&lrecv);
		} else {
			puts("recv incomplote.");
		}
		++cnt;
	}
	close(sock);
	free(buf);
  if(cnt != reqnum) printf("%d\n", cnt);
  return NULL;
}

int main(int argc, char **argv) {
	ip = (char *)argv[1];
  port = atoi(argv[2]);
	thdnum = atoi(argv[3]);
	reqnum = atoi(argv[4]);
  
	pthread_mutex_init(&lsend, NULL);
  pthread_mutex_init(&lrecv, NULL);
  
	pthread_t *tid = (pthread_t *)malloc(thdnum * sizeof(pthread_t));
	for(int i = 0; i < thdnum; ++i) {
		pthread_create(tid+i, NULL, clientProc, tid+i);	
		usleep(1000);
	}
	for(int i = 0; i < thdnum; ++i) {
		pthread_join(*(tid+i), NULL);
	}
	printf("%d %d\n", nsend, nrecv);
  free(tid);
  
  return 0;
}
