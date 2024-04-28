#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

/**
 * Main function for "Paper, Scissors, Rock".
 * 
 * @param arg1 number of command-line arguments.
 * @param arg2 array of strings with command-line arguments.
 * @return exit status of program.
 */
int main(int arg1, char *arg2[]) {
    if (arg1 != 2) {
        fprintf(stderr, "Usage: %s <number_of_rounds>\n", arg2[0]);
        exit(EXIT_FAILURE);
    }

    printf("Written by: Abraham J. Reines\n");
    printf("Paper, Scissors, Rock: %s iterations\n", arg2[1]);

    pid_t pid = fork();
    if (pid == 0) {
        // Launch referee
        execl("./referee", "referee", arg2[1], (char *)NULL);
        perror("Failed to execute referee");
        exit(EXIT_FAILURE);
    }

    int status;
    waitpid(pid, &status, 0);  // Wait for referee to finish
    // if (WIFEXITED(status)) {
    //     printf("Game completed successfully.\n");
    // }

    return EXIT_SUCCESS;
}
