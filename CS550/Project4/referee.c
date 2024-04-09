/**
 * @file referee.c
 * @brief Referee for a Paper Scissors Rock game using UNIX socket programming.
 * @author Abraham Reines
 * @date Mon Apr  8 15:47:11 PDT 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 4444

/* Function Prototypes */
void setup_server_socket(int *server_fd, struct sockaddr_in *address);
void start_game_loop(int server_fd, int rounds);
void handle_game_round(int socket);

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <number of rounds>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int server_fd;
    struct sockaddr_in address;
    int rounds = atoi(argv[1]);

    setup_server_socket(&server_fd, &address);
    start_game_loop(server_fd, rounds);

    return EXIT_SUCCESS;
}

/**
 * Sets up the server socket.
 * @param server_fd Pointer to the server file descriptor.
 * @param address Pointer to the sockaddr_in structure for binding.
 */
void setup_server_socket(int *server_fd, struct sockaddr_in *address) {
    if ((*server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Bind the socket to an address
    address->sin_family = AF_INET;
    address->sin_addr.s_addr = INADDR_ANY;
    address->sin_port = htons(PORT);

    if (bind(*server_fd, (struct sockaddr *)address, sizeof(*address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for connections
    if (listen(*server_fd, 2) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    printf("Referee started, waiting for players...\n");
}

/**
 * Starts the game loop for the specified number of rounds.
 * @param server_fd Server file descriptor.
 * @param rounds Number of game rounds.
 */
void start_game_loop(int server_fd, int rounds) {
    for (int currentRound = 0; currentRound < rounds; ++currentRound) {
        printf("Round %d of %d\n", currentRound + 1, rounds);
        
        int player_socket;
        struct sockaddr_in player_address;
        int addrlen = sizeof(player_address);

        if ((player_socket = accept(server_fd, (struct sockaddr *)&player_address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }

        handle_game_round(player_socket);
        // Close the player socket after handling the round
        close(player_socket);
    }

    printf("Game over. Final scores: ...\n"); // Implement score tracking and display
}

/**
 * Handles a single game round communication with the player.
 * @param socket Player socket file descriptor.
 */
void handle_game_round(int socket) {
    // Placeholder for communication with players, determining the winner, and score management.
}
