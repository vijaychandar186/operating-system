// Lab 06 - Dining Philosopher Problem using Semaphores
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define N         5
#define THINKING  0
#define HUNGRY    1
#define EATING    2
#define LEFT      ((id + N - 1) % N)
#define RIGHT     ((id + 1) % N)

int state[N];
int phil[N] = {0, 1, 2, 3, 4};

sem_t mutex;
sem_t S[N];

void test(int id) {
    if (state[id] == HUNGRY &&
        state[LEFT]  != EATING &&
        state[RIGHT] != EATING) {
        state[id] = EATING;
        printf("Philosopher %d takes fork %d and %d\n", id + 1, LEFT + 1, id + 1);
        printf("Philosopher %d is Eating\n", id + 1);
        sem_post(&S[id]);
    }
}

void take_fork(int id) {
    sem_wait(&mutex);
    state[id] = HUNGRY;
    printf("Philosopher %d is Hungry\n", id + 1);
    test(id);
    sem_post(&mutex);
    sem_wait(&S[id]);
    sleep(1);
}

void put_fork(int id) {
    sem_wait(&mutex);
    state[id] = THINKING;
    printf("Philosopher %d putting fork %d and %d down\n", id + 1, LEFT + 1, id + 1);
    printf("Philosopher %d is Thinking\n", id + 1);
    test(LEFT);
    test(RIGHT);
    sem_post(&mutex);
}

void* philosopher(void* arg) {
    int id = *(int*)arg;
    // Each philosopher eats 3 times then stops (avoid infinite loop in demo)
    for (int i = 0; i < 3; i++) {
        sleep(1);
        take_fork(id);
        sleep(1);
        put_fork(id);
    }
    return NULL;
}

int main() {
    pthread_t thread_id[N];
    sem_init(&mutex, 0, 1);
    for (int i = 0; i < N; i++) sem_init(&S[i], 0, 0);

    printf("=== Dining Philosopher Problem (Semaphore) ===\n\n");
    for (int i = 0; i < N; i++) {
        state[i] = THINKING;
        printf("Philosopher %d is thinking\n", i + 1);
        pthread_create(&thread_id[i], NULL, philosopher, &phil[i]);
    }

    for (int i = 0; i < N; i++) pthread_join(thread_id[i], NULL);

    printf("\nAll philosophers finished.\n");
    sem_destroy(&mutex);
    for (int i = 0; i < N; i++) sem_destroy(&S[i]);
    return 0;
}
