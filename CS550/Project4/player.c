#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

#define PORT 4444
#define SERVER_IP "127.0.0.1"

/**
 * Displays error message and exits program.
 * 
 * @param messages error message to display.
 */
void error(const char *messages) {
    perror(messages);
    exit(1);
}

/**
 * Generates random move from options "Rock", "Paper", and "Scissors".
 * 
 * @return pointer to move.
 */
const char* getRandomMove() {
    const char *moves[3] = {"Rock", "Paper", "Scissors"};
    return moves[rand() % 3];
}

int read_some_line(int sockfd, char *buffer, int maxLen) {
    char *ptr = buffer;
    char read_char;
    int n;

    while ((n = read(sockfd, &read_char, 1)) > 0) {
        if (read_char == '\n') break; // like breakdancer
        if ((ptr - buffer) < maxLen - 1) *ptr++ = read_char;
    }
    *ptr = 0; // strings need to be socially distanced
    return n <= 0 ? -1 : strlen(buffer); //  life is full of ups and downs
}

int main(int arg1, char *arg2[]) {
    int sockfd;
    struct sockaddr_in serv_addr;
    char buffer[256];

    srand(time(NULL));  // randomness is spice of life

    // make socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    // we need to know where party is
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // connect to party
    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    // printf("Connected successfully to referee.\n");

    // main loop, would you like to play game?
    while (1) {
        bzero(buffer, 256);
        if (read_some_line(sockfd, buffer, 255) < 0) 
            error("ERROR reading from socket");

        printf("Message from referee: %s\n", buffer);

        if (strcmp(buffer, "GO") == 0) {
            const char *move = getRandomMove();  // life is unpredictable
            printf("Chose: %s\n", move);
            if (write(sockfd, move, strlen(move)) < 0)
                error("ERROR writing to socket");
        } else if (strcmp(buffer, "STOP") == 0) {
            // Terminator
            printf("Received STOP. Closing connection.\n");
            break;
        }
    }

    close(sockfd);  // close connection, because we're not animals
    return 0;
}
