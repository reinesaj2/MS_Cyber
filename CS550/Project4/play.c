/**
 * @file play.c
 * @brief Coordinator for a Paper Scissors Rock game using UNIX socket programming.
 * @author Abraham J. Reines
 * @date Mon Apr 8 15:47:11 PDT 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>  // For UNIX domain sockets
#include <string.h>

/* Function Prototypes */
void launch_referee(const char *turns, const char *write_end);
void launch_players(int num_players);
void wait_for_children(int num_children);
void start_score_listener(int *server_fd, struct sockaddr_un *address);
void receive_scores(int *scores);

// Global server file descriptor for the UNIX socket
int server_fd;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_turns>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    printf("Written by: Abraham J. Reines\n");
    printf("Paper, Scissors, Rock: %s iterations\n", argv[1]);

    // Start the score listener before launching any processes
    struct sockaddr_un server_address;
    start_score_listener(&server_fd, &server_address);

    // Create a pipe to synchronize the start of the game
    int pipefd[2];
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    // Launch referee process
    char write_end_str[10];
    sprintf(write_end_str, "%d", pipefd[1]);
    launch_referee(argv[1], write_end_str);

    // Launch two player processes
    launch_players(2);

    // Close the write-end of the pipe, wait for the referee to start
    close(pipefd[1]);

    // Wait for a signal from the referee to proceed
    char buf;
    read(pipefd[0], &buf, 1);
    close(pipefd[0]);  // Close the read-end of the pipe as it's no longer needed

    // Wait for the referee and players to finish their execution
    wait_for_children(3); // We have 3 child processes: 1 referee and 2 players

    // Receive the scores from the referee via the score listener
    int scores[2] = {0};
    receive_scores(scores);

    // Clean up the server socket
    unlink(server_address.sun_path);
    close(server_fd);

    // Output the final score
    printf("Final Score:\n");
    printf("Player 1: %d\n", scores[0]);
    printf("Player 2: %d\n", scores[1]);

    return EXIT_SUCCESS;
}

/**
 * Launches the referee process.
 * @param turns Number of game turns.
 */
void launch_referee(const char *turns, const char *write_end) {
    if (fork() == 0) {
        execl("./referee", "referee", turns, write_end, (char *)NULL);
        perror("Failed to launch referee");
        exit(EXIT_FAILURE);
    }
}

/**
 * Launches a player process.
 */
void launch_players(int num_players) {
    for (int i = 0; i < num_players; ++i) {
        pid_t pid = fork();
        if (pid == 0) {
            // Construct the player ID string
            char player_id[10];
            sprintf(player_id, "%d", i + 1);
            // Replace "player" with the appropriate path if not in the current directory
            execl("./player", "player", player_id, (char *)NULL);
            perror("execl failed to launch player");
            exit(EXIT_FAILURE);
        } else if (pid < 0) {
            perror("fork");
            exit(EXIT_FAILURE);
        }
    }
}

void start_score_listener(int *server_fd, struct sockaddr_un *address) {
    // Create a socket
    *server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (*server_fd == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Set up the address structure
    memset(address, 0, sizeof(struct sockaddr_un));
    address->sun_family = AF_UNIX;
    const char *sock_path = "/tmp/psr_scores.sock";
    strncpy(address->sun_path, sock_path, sizeof(address->sun_path) - 1);

    // Unlink before binding to clean up from previous executions
    unlink(sock_path);

    // Bind the socket to the address
    if (bind(*server_fd, (struct sockaddr *)address, sizeof(struct sockaddr_un)) == -1) {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(*server_fd, 5) == -1) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
}

void receive_scores(int *scores) {
    int client_fd;
    struct sockaddr_un client_address;
    socklen_t client_address_length = sizeof(struct sockaddr_un);

    // Accept a connection from the referee
    client_fd = accept(server_fd, (struct sockaddr *)&client_address, &client_address_length);
    if (client_fd == -1) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    // Read the scores from the referee
    if (read(client_fd, scores, sizeof(int) * 2) != sizeof(int) * 2) {
        perror("read");
        exit(EXIT_FAILURE);
    }

    close(client_fd);
}

/**
 * Waits for all child processes to complete.
 * @param num_children The number of child processes to wait for.
 */
void wait_for_children(int num_children) {
    int status;
    while (num_children > 0) {
        wait(&status);  // This call can be more sophisticated with error checking
        num_children--;
    }
}
