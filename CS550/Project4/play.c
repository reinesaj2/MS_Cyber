/**
 * @file play.c
 * @brief Coordinator for a Paper Scissors Rock game using UNIX socket programming.
 * @author Abraham Reines
 * @date Mon Apr  8 15:47:11 PDT 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

/* Function Prototypes */
void initiate_socket_communication();
void launch_referee(const char *turns);
void launch_player();
void wait_for_children();

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_turns>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int turns = atoi(argv[1]);

    // Initialize socket communication
    initiate_socket_communication();

    // Launch referee process
    launch_referee(argv[1]);

    // Launch two player processes
    for (int i = 0; i < 2; i++) {
        launch_player();
    }

    // Wait for all child processes to complete
    wait_for_children();

    return EXIT_SUCCESS;
}

/**
 * Initializes the socket communication between the coordinator, players, and the referee.
 */
void initiate_socket_communication() {
    // Placeholder for socket initialization code
}

/**
 * Launches the referee process.
 * @param turns Number of game turns.
 */
void launch_referee(const char *turns) {
    if (fork() == 0) {
        if (execl("./referee", "referee", turns, (char *)NULL) == -1) {
            perror("Failed to launch referee");
            exit(EXIT_FAILURE);
        }
    }
}

/**
 * Launches a player process.
 */
void launch_player() {
    if (fork() == 0) {
        if (execl("./player", "player", (char *)NULL) == -1) {
            perror("Failed to launch player");
            exit(EXIT_FAILURE);
        }
    }
}

/**
 * Waits for all child processes to complete.
 */
void wait_for_children() {
    for (int i = 0; i < 3; i++) {
        wait(NULL);
    }
}
