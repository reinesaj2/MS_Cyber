/**
 * @file readstr.c
 * @brief Utility function to read a string from a file descriptor until a newline character.
 * @author Abraham Reines
 * @date Mon Apr  8 15:47:11 PDT 2024
 */

#include <unistd.h>

/**
 * Reads characters from a file descriptor into a buffer until a newline is encountered.
 * 
 * @param fd The file descriptor from which to read.
 * @param str The buffer where the read string will be stored.
 * 
 * Notes:
 * - The function assumes `str` has enough space to store the read data.
 * - The string stored in `str` will be null-terminated.
 * - If a newline is read, it is not included in the stored string.
 * - The function stops reading if either a newline is encountered or an error occurs.
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
            // End loop if readResult is 0 (EOF) or less (error)
            break;
        }
    }

    *str = '\0'; // Null-terminate the string
}