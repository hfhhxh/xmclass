#!/bin/sh
gcc -c ae.c -o ae.o
gcc -c client.c -o client.o -lpthread -std=c11
gcc client.o -o client -lpthread -std=c11
gcc -c server.c -o server.o -lpthread -std=c11
gcc ae.o server.o -o server -lpthread -std=c11
