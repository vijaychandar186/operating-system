// Lab 07 - Process Creation using fork(), getpid(), getppid(), wait(), exit()
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    printf("=== fork() System Call Demo ===\n\n");

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return EXIT_FAILURE;
    } else if (pid == 0) {
        // Child process
        printf("Child  => PID: %d, PPID: %d\n", getpid(), getppid());
        printf("Child  => Doing some work...\n");
        sleep(1);
        printf("Child  => Done. Exiting.\n");
        exit(EXIT_SUCCESS);
    } else {
        // Parent process
        printf("Parent => PID: %d\n", getpid());
        printf("Parent => Child PID is %d. Waiting...\n", pid);
        int status;
        wait(&status);
        if (WIFEXITED(status))
            printf("Parent => Child exited with status %d\n", WEXITSTATUS(status));
        printf("Parent => Child process finished.\n");
    }

    return EXIT_SUCCESS;
}
