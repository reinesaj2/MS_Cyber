#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 4444

/**
 * Sends a message to specified socket.
 * 
 * @param socket socket to send message to.
 * @param message message to send.
 */
void send_player_messages(int socket, char *message) {
    char formatted_message[1024];
    snprintf(formatted_message, sizeof(formatted_message), "%s\n", message);
    if (send(socket, formatted_message, strlen(formatted_message), 0) < 0) {
        perror("send failed");
        exit(EXIT_FAILURE);
    }
}

/**
 * main function of referee program.
 * 
 * @param arg1  number of command-line arguments.
 * @param arg2  array of command-line arguments.
 * @return  exit status of program.
 */
int main(int arg1, char *arg2[]) {
    if (arg1 != 2) {
        fprintf(stderr, "Usage: %s <number_of_rounds>\n", arg2[0]);
        exit(EXIT_FAILURE);
    }

    int rounds = atoi(arg2[1]);
    int server_fd, player_needs_sock[2];
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char choices[2][10];  // store choices from both players
    int scores[2] = {0, 0};  // Score player 1 and player 2

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

    for (int i = 0; i < 2; i++) {
        player_needs_sock[i] = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (player_needs_sock[i] < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }
        printf("          Player %d: Ready\n", i + 1);
        send_player_messages(player_needs_sock[i], "READY");
    }

    for (int round = 0; round < rounds; round++) {
        printf("Go Players [%d]:\n", round + 1);
        for (int j = 0; j < 2; j++) {
            send_player_messages(player_needs_sock[j], "GO");
            memset(choices[j], 0, sizeof(choices[j]));
            if (recv(player_needs_sock[j], choices[j], sizeof(choices[j]), 0) < 0) {
                perror("recv failed");
                exit(EXIT_FAILURE);
            }
            printf("          Player %d: %s\n", j + 1, choices[j]);
        }

        int result = 0; // 0 = Draw, 1 = player 1 Wins, 2 = player 2 Wins
        if (strcmp(choices[0], choices[1]) == 0) {
            printf("          Players Draw\n");
        } else if ((strcmp(choices[0], "Rock") == 0 && strcmp(choices[1], "Scissors") == 0) ||
                   (strcmp(choices[0], "Scissors") == 0 && strcmp(choices[1], "Paper") == 0) ||
                   (strcmp(choices[0], "Paper") == 0 && strcmp(choices[1], "Rock") == 0)) {
            printf("          Player 1 Wins\n");
            scores[0]++;
            result = 1;
        } else {
            printf("          Player 2 Wins\n");
            scores[1]++;
            result = 2;
        }

        if (result == 0) {
            send_player_messages(player_needs_sock[0], "Draw");
            send_player_messages(player_needs_sock[1], "Draw");
        } else if (result == 1) {
            send_player_messages(player_needs_sock[0], "Win");
            send_player_messages(player_needs_sock[1], "Lose");
        } else {
            send_player_messages(player_needs_sock[0], "Lose");
            send_player_messages(player_needs_sock[1], "Win");
        }
    }

    printf("Final Score: \n          Player 1: %d \n          Player 2: %d\n", scores[0], scores[1]);
    if (scores[0] > scores[1]) {
        printf("Winner is Player 1!\n");
    } else if (scores[1] > scores[0]) {
        printf("Winner is Player 2!\n");
    } else {
        printf("Players Draw\n");
    }

    for (int i = 0; i < 2; i++) {
        send_player_messages(player_needs_sock[i], "STOP");
        close(player_needs_sock[i]);
    }

    // printf("Game completed, server shutting down.\n");
    close(server_fd);
    return 0;
}
