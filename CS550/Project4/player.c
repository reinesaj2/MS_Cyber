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
void connect_to_referee(int *sockfd, struct sockaddr_in *serv_addr, int player_id);
void play_game(int sockfd);
char *choose_move(int sockfd);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <player_id>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    int player_id = atoi(argv[1]);

    int sockfd;
    struct sockaddr_in serv_addr;

    // Initialize random number generator
    srand(time(NULL));

    // Pass player_id to the connect_to_referee function
    connect_to_referee(&sockfd, &serv_addr, player_id);
    play_game(sockfd);

    close(sockfd);
    return EXIT_SUCCESS;
}

void connect_to_referee(int *sockfd, struct sockaddr_in *serv_addr, int player_id) {
    *sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (*sockfd < 0) {
        perror("Error creating socket");
        exit(EXIT_FAILURE);
    }

    memset(serv_addr, 0, sizeof(*serv_addr));
    serv_addr->sin_family = AF_INET;
    serv_addr->sin_port = htons(PORT);

    if (inet_pton(AF_INET, SERVER_IP, &serv_addr->sin_addr) <= 0) {
        perror("Invalid address/Address not supported");
        exit(EXIT_FAILURE);
    }

    if (connect(*sockfd, (struct sockaddr *)serv_addr, sizeof(*serv_addr)) < 0) {
        perror("Connection Failed");
        exit(EXIT_FAILURE);
    }

    // Send initial "READY" message
    send(*sockfd, "READY", strlen("READY"), 0);

    // After sending "READY" message
    fflush(stdout);  // Make sure the "Ready" message is printed out immediately


    // Print ready message without socket number
    printf("Player %d: Ready\n", player_id);
}

char *choose_move(int sockfd) {
    static char *moves[] = {"PAPER", "SCISSORS", "ROCK"};
    int choice = rand() % 3;

    return moves[choice];
}

void play_game(int sockfd) {
    char buffer[1024];
    
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        // Removed the delay for Player 2
        
        if (read(sockfd, buffer, sizeof(buffer)) <= 0) {
            perror("Read error or connection closed by server");
            exit(EXIT_FAILURE);
        }

        ssize_t numBytes = read(sockfd, buffer, sizeof(buffer) - 1);
        if (numBytes <= 0) {
            perror("Read error or connection closed by server");
            exit(EXIT_FAILURE);
        }

        buffer[numBytes] = '\0'; // Null-terminate the string

        if (strcmp(buffer, "GO") == 0) {
            char *move = choose_move();
            printf("%s\n", move); // This line is for debugging purposes only
            fflush(stdout);
            if (send(sockfd, move, strlen(move), 0) < 0) {
                perror("Error sending move");
                exit(EXIT_FAILURE);
            }
        } else if (strcmp(buffer, "END") == 0) {
            // Handle 'END' command
            break;
        }
    }
}