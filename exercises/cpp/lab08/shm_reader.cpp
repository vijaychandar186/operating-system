// Lab 08 - Shared Memory IPC (Reader)
#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <cstdio>
using namespace std;

int main() {
    key_t key = ftok("shmfile", 65);
    if (key == -1) { perror("ftok (run shm_writer first)"); return 1; }

    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);
    if (shmid == -1) { perror("shmget"); return 1; }

    char* str = (char*)shmat(shmid, nullptr, 0);
    if (str == (char*)-1) { perror("shmat"); return 1; }

    printf("Data read from shared memory: \"%s\"\n", str);

    shmdt(str);
    // Destroy shared memory segment
    shmctl(shmid, IPC_RMID, nullptr);
    printf("Shared memory segment destroyed.\n");
    return 0;
}
