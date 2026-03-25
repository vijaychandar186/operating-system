// Lab 05 - Reader-Writer Problem using Monitors (pthread)
#include <iostream>
#include <pthread.h>
#include <unistd.h>
using namespace std;

class Monitor {
private:
    int rcnt;   // active readers
    int wcnt;   // active writers
    int waitr;  // waiting readers
    int waitw;  // waiting writers
    pthread_cond_t  canread;
    pthread_cond_t  canwrite;
    pthread_mutex_t condlock;

public:
    Monitor() : rcnt(0), wcnt(0), waitr(0), waitw(0) {
        pthread_cond_init(&canread,  NULL);
        pthread_cond_init(&canwrite, NULL);
        pthread_mutex_init(&condlock, NULL);
    }

    ~Monitor() {
        pthread_cond_destroy(&canread);
        pthread_cond_destroy(&canwrite);
        pthread_mutex_destroy(&condlock);
    }

    void beginread(int id) {
        pthread_mutex_lock(&condlock);
        // Wait if a writer is active or waiting
        while (wcnt == 1 || waitw > 0) {
            waitr++;
            pthread_cond_wait(&canread, &condlock);
            waitr--;
        }
        rcnt++;
        cout << "Reader " << id << " is reading\n";
        pthread_mutex_unlock(&condlock);
        pthread_cond_broadcast(&canread);
    }

    void endread(int id) {
        pthread_mutex_lock(&condlock);
        if (--rcnt == 0)
            pthread_cond_signal(&canwrite);
        pthread_mutex_unlock(&condlock);
    }

    void beginwrite(int id) {
        pthread_mutex_lock(&condlock);
        while (wcnt == 1 || rcnt > 0) {
            waitw++;
            pthread_cond_wait(&canwrite, &condlock);
            waitw--;
        }
        wcnt = 1;
        cout << "Writer " << id << " is writing\n";
        pthread_mutex_unlock(&condlock);
    }

    void endwrite(int id) {
        pthread_mutex_lock(&condlock);
        wcnt = 0;
        if (waitr > 0)
            pthread_cond_broadcast(&canread);
        else
            pthread_cond_signal(&canwrite);
        pthread_mutex_unlock(&condlock);
    }
};

Monitor M;

void* reader(void* arg) {
    int id = *(int*)arg;
    for (int c = 0; c < 3; c++) {
        usleep(100);
        M.beginread(id);
        usleep(50);
        M.endread(id);
    }
    return NULL;
}

void* writer(void* arg) {
    int id = *(int*)arg;
    for (int c = 0; c < 2; c++) {
        usleep(150);
        M.beginwrite(id);
        usleep(50);
        M.endwrite(id);
    }
    return NULL;
}

int main() {
    const int NUM = 5;
    pthread_t r[NUM], w[NUM];
    int id[NUM];

    cout << "=== Reader-Writer Problem (Monitor) ===\n\n";
    for (int i = 0; i < NUM; i++) {
        id[i] = i + 1;
        pthread_create(&r[i], NULL, reader, &id[i]);
        pthread_create(&w[i], NULL, writer, &id[i]);
    }
    for (int i = 0; i < NUM; i++) pthread_join(r[i], NULL);
    for (int i = 0; i < NUM; i++) pthread_join(w[i], NULL);

    cout << "\nAll readers and writers finished.\n";
    return 0;
}
