#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_rounds>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    printf("Written by: Abraham Reines\n");
    printf("Paper, Scissors, Rock: %s iterations\n", argv[1]);

    pid_t pid = fork();
    if (pid == 0) {
        // Launch the referee
        execl("./referee", "referee", argv[1], (char *)NULL);
        perror("Failed to exec referee");
        exit(EXIT_FAILURE);
    }

    int status;
    waitpid(pid, &status, 0);  // Wait for the referee to finish
    // if (WIFEXITED(status)) {
    //     printf("Game completed successfully.\n");
    // }

    return EXIT_SUCCESS;
}
