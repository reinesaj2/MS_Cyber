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
#include <sys/un.h>

#define PORT 4444
#define NOT_CONNECTED 0
#define CONNECTED     1
#define READY         2

/* Function Prototypes */
void setup_server_socket(int *server_fd, struct sockaddr_in *address);
void start_game_loop(int server_fd, int rounds);
void handle_game_round(int player1_socket, int player2_socket, int round_count, int scores[]);
int compare_moves(const char *move1, const char *move2);
void readstr(int fd, char *str);
void send_scores_to_play(int *scores);

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <number of rounds> <pipe write end>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int server_fd;
    struct sockaddr_in address;
    int rounds = atoi(argv[1]);
    int write_end = atoi(argv[2]);

    // This will hold the scores for each player
    int scores[2] = {0, 0};  // Move the score array here, so it's in scope for send_scores_to_play

    setup_server_socket(&server_fd, &address);
    // Signal to the play process that the referee is ready
    write(write_end, "1", 1);
    close(write_end);
    
    // Start the game loop and play the rounds
    start_game_loop(server_fd, rounds);

    // Send the scores back to the play process
    send_scores_to_play(scores);

    // Close the server socket
    close(server_fd);

    return EXIT_SUCCESS;
}

void setup_server_socket(int *server_fd, struct sockaddr_in *address) {
    *server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (*server_fd < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    int opt = 1;
    // Forcefully attaching socket to the port 4444
    if (setsockopt(*server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    address->sin_family = AF_INET;
    address->sin_addr.s_addr = INADDR_ANY;
    address->sin_port = htons(PORT);

    // Binding the socket to the port 4444
    if (bind(*server_fd, (struct sockaddr *)address, sizeof(*address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(*server_fd, 2) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    // printf("Referee started, waiting for players...\n");
}

void start_game_loop(int server_fd, int rounds) {
    int player_sockets[2] = {-1, -1};
    struct sockaddr_in player_address;
    socklen_t addrlen = sizeof(player_address);
    int scores[2] = {0, 0};

    // Accept connections from both players
    for (int i = 0; i < 2; ++i) {
        player_sockets[i] = accept(server_fd, (struct sockaddr *)&player_address, &addrlen);
        if (player_sockets[i] < 0) {
            perror("Accept player failed");
            exit(EXIT_FAILURE);
        }
    }

    // Wait for both players to send "READY"
    char buffer[10];
    for (int i = 0; i < 2; ++i) {
        memset(buffer, 0, sizeof(buffer)); // Clear the buffer for clean read
        readstr(player_sockets[i], buffer);
        if (strcmp(buffer, "READY") != 0) {
            fprintf(stderr, "Error: Player %d not ready.\n", i + 1);
            exit(EXIT_FAILURE);
        }
        printf("Player %d: Ready\n", i + 1);
        fflush(stdout);  // Ensure immediate output
    }

    // Now that both players are ready, start the game rounds
    for (int round = 0; round < rounds; round++) {
        handle_game_round(player_sockets[0], player_sockets[1], round, scores);
    }

    printf("Game over. Final scores: Player 1 - %d, Player 2 - %d\n", scores[0], scores[1]);
    fflush(stdout);  // Ensure immediate output
    close(player_sockets[0]);
    close(player_sockets[1]);
}

void handle_game_round(int player1_socket, int player2_socket, int round_count, int scores[]) {
    // Check that player1_socket and player2_socket are valid socket descriptors
    if (player1_socket < 0 || player2_socket < 0) {
        fprintf(stderr, "Error: Invalid socket descriptor.\n");
        return;
    }

    // Check that round_count is a non-negative integer
    if (round_count < 0) {
        fprintf(stderr, "Error: Invalid round count.\n");
        return;
    }

    // Check that scores is an array of at least two integers
    if (scores == NULL) {
        fprintf(stderr, "Error: Scores array is NULL.\n");
        return;
    }

    char move1[10], move2[10];
    printf("Go Players [%d]\n", round_count + 1);
    fflush(stdout);  // Ensure immediate output

    // Send 'GO' command to both players
    if (send(player1_socket, "GO\n", 3, 0) < 0 || send(player2_socket, "GO\n", 3, 0) < 0) {
        perror("Error sending GO command");
        exit(EXIT_FAILURE);
    }

    // Read the moves from both players
    readstr(player1_socket, move1);
    readstr(player2_socket, move2);
    
    printf("Player 1 move: %s\n", move1);
    printf("Player 2 move: %s\n", move2);

    int result = compare_moves(move1, move2);
    switch (result) {
        case 0: printf("Players Draw\n"); break;
        case 1: scores[0]++; printf("Player 1 Wins\n"); break;
        case 2: scores[1]++; printf("Player 2 Wins\n"); break;
    }
    printf("Player 1 score: %d\n", scores[0]);
    printf("Player 2 score: %d\n", scores[1]);
}

int compare_moves(const char *move1, const char *move2) {
    if (strcmp(move1, move2) == 0) return 0;
    if ((strcmp(move1, "ROCK") == 0 && strcmp(move2, "SCISSORS") == 0) ||
        (strcmp(move1, "SCISSORS") == 0 && strcmp(move2, "PAPER") == 0) ||
        (strcmp(move1, "PAPER") == 0 && strcmp(move2, "ROCK") == 0)) {
        return 1;
    }
    return 2;
}

void send_scores_to_play(int *scores) {
    int sockfd;
    struct sockaddr_un address;

    // Create a socket
    sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Set up the address structure
    memset(&address, 0, sizeof(struct sockaddr_un));
    address.sun_family = AF_UNIX;
    strncpy(address.sun_path, "/tmp/psr_scores.sock", sizeof(address.sun_path) - 1);

    // Connect to the play process's server socket
    if (connect(sockfd, (struct sockaddr *)&address, sizeof(struct sockaddr_un)) == -1) {
        perror("connect");
        exit(EXIT_FAILURE);
    }

    // Send the scores
    if (write(sockfd, scores, sizeof(int) * 2) != sizeof(int) * 2) {
        perror("write");
        exit(EXIT_FAILURE);
    }

    close(sockfd);
}