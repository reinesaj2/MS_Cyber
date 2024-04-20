#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 4444

void send_message(int socket, char *message) {
    if (send(socket, message, strlen(message), 0) < 0) {
        perror("send failed");
        exit(EXIT_FAILURE);
    }
    // printf("Sent to player socket %d: %s\n", socket, message);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_rounds>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int rounds = atoi(argv[1]);
    int server_fd, player_socket[2];
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char choices[2][10];  // Added to store choices from both players

    // printf("Setting up server on port %d...\n", PORT);

    // Setup the server socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 2) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    // printf("Server is listening...\n");

    // Accept connections from two players
    for (int i = 0; i < 2; i++) {
        player_socket[i] = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (player_socket[i] < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }
        printf("Player %d connected.\n", i + 1);
        send_message(player_socket[i], "READY");
    }

    // Main game loop
    for (int round = 0; round < rounds; round++) {
        printf("Starting Round %d:\n", round + 1);
        for (int j = 0; j < 2; j++) {
            send_message(player_socket[j], "GO");
            memset(choices[j], 0, sizeof(choices[j]));  // Clear previous choice
            if (recv(player_socket[j], choices[j], sizeof(choices[j]), 0) < 0) {
                perror("recv failed");
                exit(EXIT_FAILURE);
            }
            printf("Player %d chose: %s\n", j + 1, choices[j]);
        }

        // Game decision logic
        int result = 0; // 0 = draw, 1 = player 1 wins, 2 = player 2 wins
        if (strcmp(choices[0], choices[1]) == 0) {
            printf("Result: Draw\n");
            result = 0; // Draw
        } else if ((strcmp(choices[0], "ROCK") == 0 && strcmp(choices[1], "SCISSORS") == 0) ||
                   (strcmp(choices[0], "SCISSORS") == 0 && strcmp(choices[1], "PAPER") == 0) ||
                   (strcmp(choices[0], "PAPER") == 0 && strcmp(choices[1], "ROCK") == 0)) {
            printf("Player 1 wins\n");
            result = 1; // Player 1 wins
        } else {
            printf("Player 2 wins\n");
            result = 2; // Player 2 wins
        }

        // Send results back to players
        if (result == 0) {
            send_message(player_socket[0], "DRAW");
            send_message(player_socket[1], "DRAW");
        } else if (result == 1) {
            send_message(player_socket[0], "WIN");
            send_message(player_socket[1], "LOSE");
        } else {
            send_message(player_socket[0], "LOSE");
            send_message(player_socket[1], "WIN");
        }
    }

    // Send STOP message to players and close sockets
    for (int i = 0; i < 2; i++) {
        send_message(player_socket[i], "STOP");
        close(player_socket[i]);
    }

    printf("Game completed, server shutting down.\n");
    close(server_fd);
    return 0;
}
