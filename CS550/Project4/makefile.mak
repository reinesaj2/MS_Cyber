CC = gcc
CFLAGS = -g -Wall
OBJS = play.o referee.o player.o readstr.o

all: play referee player

play: play.o
	$(CC) $(CFLAGS) play.o -o play

referee: referee.o readstr.o
	$(CC) $(CFLAGS) referee.o readstr.o -o referee

player: player.o readstr.o
	$(CC) $(CFLAGS) player.o readstr.o -o player

play.o: play.c
	$(CC) $(CFLAGS) -c play.c -o play.o

referee.o: referee.c
	$(CC) $(CFLAGS) -c referee.c -o referee.o

player.o: player.c
	$(CC) $(CFLAGS) -c player.c -o player.o

readstr.o: readstr.c
	$(CC) $(CFLAGS) -c readstr.c -o readstr.o

clean:
	rm -f $(OBJS) play referee player
