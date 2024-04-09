all: play referee player

play: play.c
	gcc play.c -o play

referee: referee.c readstr.o
	gcc referee.c readstr.o -o referee

player: player.c readstr.o
	gcc player.c readstr.o -o player

readstr.o: readstr.c
	gcc -c readstr.c

clean:
	rm -f play referee player readstr.o
