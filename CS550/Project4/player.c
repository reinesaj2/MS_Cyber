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

void error(const char *msg) {
    perror(msg);
    exit(1);
}

const char* getRandomMove() {
    const char *moves[3] = {"ROCK", "PAPER", "SCISSORS"};
    return moves[rand() % 3];
}

int main(int argc, char *argv[]) {
    int sockfd;
    struct sockaddr_in serv_addr;
    char buffer[256];

    srand(time(NULL));  // Seed the random number generator

    // Creating the socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    // Define the server address
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // Connect to the server
    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    // printf("Connected successfully to the referee.\n");

    // Main loop to listen for commands from the referee
    while (1) {
        bzero(buffer, 256);
        if (read(sockfd, buffer, 255) < 0) 
            error("ERROR reading from socket");

        printf("Message from referee: %s\n", buffer);

        if (strcmp(buffer, "GO") == 0) {
            // If received GO, decide on a move
            const char *move = getRandomMove();  // Get a random move
            printf("Chose: %s\n", move);
            if (write(sockfd, move, strlen(move)) < 0)
                error("ERROR writing to socket");
        } else if (strcmp(buffer, "STOP") == 0) {
            // If received STOP, terminate
            printf("Received STOP. Closing connection.\n");
            break;
        }
    }

    close(sockfd);  // Close the socket
    return 0;
}
