#include <stdio.h>

void test_start_game_loop() {
  int server_fd = 0;  // This would need to be a valid server file descriptor
  int rounds = 5;

  // Call the function to test
  start_game_loop(server_fd, rounds);

  // Add checks here to verify the function's behavior
  // This is challenging for this function because it involves network operations and user interactions
  // You might need to modify the function to make it more testable, e.g., by having it return a value that you can check
}

int main() {
  // Run the test
  test_start_game_loop();

  return 0;
}