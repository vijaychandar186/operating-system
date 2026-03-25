// Lab 09 - Message Queue IPC (Writer)
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>

#define MAX 100

struct mesg_buffer {
    long mesg_type;
    char mesg_text[MAX];
};

int main() {
    FILE* f = fopen("progfile", "w"); fclose(f);
    key_t key  = ftok("progfile", 65);
    int   msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1) { perror("msgget"); return 1; }

    struct mesg_buffer message;
    message.mesg_type = 1;

    printf("Write data to message queue: ");
    fgets(message.mesg_text, MAX, stdin);

    // Remove trailing newline
    int len = strlen(message.mesg_text);
    if (len > 0 && message.mesg_text[len-1] == '\n')
        message.mesg_text[len-1] = '\0';

    if (msgsnd(msgid, &message, sizeof(message), 0) == -1) {
        perror("msgsnd"); return 1;
    }

    printf("Message sent: \"%s\"\n", message.mesg_text);
    printf("Run msg_reader to receive the message.\n");
    return 0;
}
