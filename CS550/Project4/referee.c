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
void handle_game_round(int player1_socket, int player2_socket, int round_count, int scores[]);
int compare_moves(const char *move1, const char *move2);
void readstr(int fd, char *str); // Make sure to define this function or link with its object file

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
        printf("Server is set up at port %d\n", PORT);

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
    
    FILE *fp = fopen("ref_ready.flag", "w");
    fprintf(fp, "ready");
    fclose(fp);
    printf("Referee started, waiting for players...\n");
}

/**
 * Starts the game loop for the specified number of rounds.
 * @param server_fd Server file descriptor.
 * @param rounds Number of game rounds.
 */
void start_game_loop(int server_fd, int rounds) {
    int player1_socket, player2_socket;
    struct sockaddr_in player_address;
    socklen_t addrlen = sizeof(player_address);
    int scores[2] = {0, 0}; // Initialize scores for two players

    // Accept connections from both players
    player1_socket = accept(server_fd, (struct sockaddr *)&player_address, &addrlen);
    if (player1_socket < 0) {
        perror("accept player 1");
        exit(EXIT_FAILURE);
    }
    player2_socket = accept(server_fd, (struct sockaddr *)&player_address, &addrlen);
    if (player2_socket < 0) {
        perror("accept player 2");
        exit(EXIT_FAILURE);
    }

    // Start the game loop for the specified number of rounds
    for (int currentRound = 0; currentRound < rounds; ++currentRound) {
        handle_game_round(player1_socket, player2_socket, currentRound, scores);
    }

    // Close player sockets after the game
    close(player1_socket);
    close(player2_socket);

    printf("Game over. Final scores: Player 1 - %d, Player 2 - %d\n", scores[0], scores[1]);
}

/**
 * Handles a single game round communication with both players.
 * @param player1_socket First player's socket file descriptor.
 * @param player2_socket Second player's socket file descriptor.
 * @param round_count Current round number.
 * @param scores Array holding the scores of the players.
 */
void handle_game_round(int player1_socket, int player2_socket, int round_count, int scores[]) {
    char move1[10], move2[10];

    // Announce round
    printf("Go Players [%d]\n", round_count + 1);

    printf("Sending 'GO' to players\n");
    send(player1_socket, "GO\n", 3, 0);
    send(player2_socket, "GO\n", 3, 0);
    printf("Reading moves from players\n");
    readstr(player1_socket, move1);
    readstr(player2_socket, move2);
    printf("Player 1: %s\nPlayer 2: %s\n", move1, move2);


    // Process moves and determine the winner
    int result = compare_moves(move1, move2);
    switch (result) {
        case 0: // Tie
            printf("Players Draw\n");
            break;
        case 1: // Player 1 wins
            scores[0]++;
            printf("Player 1 Wins\n");
            break;
        case 2: // Player 2 wins
            scores[1]++;
            printf("Player 2 Wins\n");
            break;
    }
}

/**
 * Compares the moves of both players and determines the winner.
 * @param move1 First player's move.
 * @param move2 Second player's move.
 * @return Result of comparison: 0 for tie, 1 if player 1 wins, 2 if player 2 wins.
 */
int compare_moves(const char *move1, const char *move2) {
    // This is a simple comparison function that assumes valid moves are provided.
    if (strcmp(move1, move2) == 0) {
        return 0; // Tie
    }
    if ((strcmp(move1, "ROCK") == 0 && strcmp(move2, "SCISSORS") == 0) ||
        (strcmp(move1, "SCISSORS") == 0 && strcmp(move2, "PAPER") == 0) ||
        (strcmp(move1, "PAPER") == 0 && strcmp(move2, "ROCK") == 0)) {
        return 1; // Player 1 wins
    }
    return 2; // Player 2 wins
}
