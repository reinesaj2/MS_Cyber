/**
 * @file player.c
 * @brief Player for a Paper Scissors Rock game using UNIX socket programming.
 * @author Abraham Reines
 * @date Mon Apr  8 15:47:11 PDT 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#define PORT 4444
#define SERVER_IP "127.0.0.1"

/* Function Prototypes */
void connect_to_referee(int *sockfd, struct sockaddr_in *serv_addr);
void play_game(int sockfd);
char *choose_move();

int main() {
    int sockfd = 0;
    struct sockaddr_in serv_addr;

    // Initialize random number generator
    srand(time(NULL));

    connect_to_referee(&sockfd, &serv_addr);
    play_game(sockfd);

    close(sockfd);
    return 0;
}

/**
 * Establishes a connection to the referee's server socket.
 * @param sockfd Pointer to the socket file descriptor.
 * @param serv_addr Pointer to the sockaddr_in structure for the server.
 */
void connect_to_referee(int *sockfd, struct sockaddr_in *serv_addr) {
    if ((*sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    memset(serv_addr, '0', sizeof(*serv_addr));
    serv_addr->sin_family = AF_INET;
    serv_addr->sin_port = htons(PORT);

    if (inet_pton(AF_INET, SERVER_IP, &serv_addr->sin_addr) <= 0) {
        perror("Invalid address/ Address not supported");
        exit(EXIT_FAILURE);
    }

    if (connect(*sockfd, (struct sockaddr *)serv_addr, sizeof(*serv_addr)) < 0) {
        perror("Connection Failed");
        exit(EXIT_FAILURE);
    }

    // Send initial "READY" message
    send(*sockfd, "READY", strlen("READY"), 0);
}

/**
 * The main game loop, handling communications with the referee.
 * @param sockfd Socket file descriptor.
 */
void play_game(int sockfd) {
    char buffer[1024] = {0};
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        if (read(sockfd, buffer, sizeof(buffer)) < 0) {
            perror("Read error");
            exit(EXIT_FAILURE);
        }

        if (strcmp(buffer, "GO") == 0) {
            char *move = choose_move();
            send(sockfd, move, strlen(move), 0);
        } else if (strcmp(buffer, "STOP") == 0) {
            break;
        }
    }
}

/**
 * Chooses a move randomly between "PAPER", "SCISSORS", and "ROCK".
 * @return The chosen move.
 */
char *choose_move() {
    char *moves[] = {"PAPER", "SCISSORS", "ROCK"};
    int choice = rand() % 3;
    return moves[choice];
}
