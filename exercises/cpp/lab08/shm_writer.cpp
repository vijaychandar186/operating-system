// Lab 08 - Shared Memory IPC (Writer)
#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <cstring>
#include <cstdio>
using namespace std;

int main() {
    // Generate a unique key (creates "shmfile" if it doesn't exist)
    FILE* f = fopen("shmfile", "w"); fclose(f);
    key_t key = ftok("shmfile", 65);

    // Create or access shared memory segment
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);
    if (shmid == -1) { perror("shmget"); return 1; }

    // Attach to shared memory
    char* str = (char*)shmat(shmid, nullptr, 0);
    if (str == (char*)-1) { perror("shmat"); return 1; }

    cout << "Write data to shared memory: ";
    fgets(str, 100, stdin);

    // Remove trailing newline
    int len = strlen(str);
    if (len > 0 && str[len-1] == '\n') str[len-1] = '\0';

    printf("Data written to shared memory: \"%s\"\n", str);
    printf("Run shm_reader now to read the data.\n");

    shmdt(str);
    return 0;
}
