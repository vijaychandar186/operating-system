// Lab 09 - Message Queue IPC (Reader)
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#define MAX 100

struct mesg_buffer {
    long mesg_type;
    char mesg_text[MAX];
};

int main() {
    key_t key  = ftok("progfile", 65);
    if (key == -1) { perror("ftok (run msg_writer first)"); return 1; }
    int   msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1) { perror("msgget"); return 1; }

    struct mesg_buffer message;
    if (msgrcv(msgid, &message, sizeof(message), 1, 0) == -1) {
        perror("msgrcv"); return 1;
    }

    printf("Message received: \"%s\"\n", message.mesg_text);

    // Destroy the message queue
    msgctl(msgid, IPC_RMID, NULL);
    printf("Message queue destroyed.\n");
    return 0;
}
