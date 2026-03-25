// Lab 10 - Unidirectional Pipe IPC
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
    int pipefds[2];
    char writemessages[2][20] = {"Hi", "Hello"};
    char readmessage[20];

    printf("=== Unidirectional Pipe IPC ===\n\n");

    if (pipe(pipefds) == -1) {
        perror("pipe");
        return 1;
    }

    // Write message 1
    printf("Writing to pipe   - Message 1: \"%s\"\n", writemessages[0]);
    write(pipefds[1], writemessages[0], strlen(writemessages[0]) + 1);
    read(pipefds[0],  readmessage, sizeof(readmessage));
    printf("Reading from pipe - Message 1: \"%s\"\n", readmessage);

    // Write message 2
    printf("\nWriting to pipe   - Message 2: \"%s\"\n", writemessages[1]);
    write(pipefds[1], writemessages[1], strlen(writemessages[1]) + 1);
    read(pipefds[0],  readmessage, sizeof(readmessage));
    printf("Reading from pipe - Message 2: \"%s\"\n", readmessage);

    close(pipefds[0]);
    close(pipefds[1]);
    return 0;
}
