// Lab 11 - Process Overlay using execl()
// Demonstrates overlaying one process image with another.
// Compile:  g++ -o hello hello.cpp && g++ -o loop loop.cpp && g++ -o overlay overlay.cpp
// Run:      ./overlay
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int main() {
    printf("=== Process Overlay Demo ===\n\n");

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child: overlay with hello
        printf("Child  => Running Hello World program via execl\n");
        execl("./hello", "./hello", (char*)NULL);
        perror("execl hello failed"); // only reached on error
        exit(1);
    } else {
        // Parent: wait, then overlay with loop
        wait(NULL);
        printf("Parent => Running loop program via execl\n");
        execl("./loop", "./loop", "5", (char*)NULL);
        perror("execl loop failed");
    }

    return 0;
}
