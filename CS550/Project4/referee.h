#ifndef REFEREE_H
#define REFEREE_H

#include <netinet/in.h>

/* Function prototypes */

// Setup the server socket and bind it to an address
void setup_server_socket(int *server_fd, struct sockaddr_in *address);

// Start the game loop which manages rounds and player interactions
void start_game_loop(int server_fd, int rounds);

// Handle each individual round of the game, managing player moves and scoring
void handle_game_round(int player1_socket, int player2_socket, int round_count, int scores[]);

// Compare the moves from two players and determine the round outcome
int compare_moves(const char *move1, const char *move2);

// Read a string from a file descriptor until a newline character is found
void readstr(int fd, char *str);

// Send the final scores to the game coordinator process
void send_scores_to_play(int *scores);

#endif /* REFEREE_H */
