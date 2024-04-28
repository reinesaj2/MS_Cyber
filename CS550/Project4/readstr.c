/**
 * @file readstr.c
 * @brief Utility function to read a string from a file descriptor until a newline character.
 * @author Abraham Reines
 * @date Mon Apr  8 15:47:11 PDT 2024
 */

#include <unistd.h>

/**
 * Reads characters from a file descriptor into a buffer until a newline.
 * 
 * @param fd file descriptor to read.
 * @param str buffer where string will be stored.
 * 
 * Notes:
 * - function assumes `str` has space to store read data.
 * - string stored in `str` will be terminated.
 * - If a newline is read, it is not included in stored string.
 * - function stops reading if a newline is encountered or an error happens.
 */
void readstr(int fd, char *str) {
    char ch;
    ssize_t readResult;

    while (1) {
        readResult = read(fd, &ch, 1);
        
        if (readResult > 0) {
            if (ch == '\n') break; // Stop at newline
            *str++ = ch; // Store character and move pointer
        } else {
            // End loop if readResult is 0 or less
            break;
        }
    }

    *str = '\0'; // terminate string
}