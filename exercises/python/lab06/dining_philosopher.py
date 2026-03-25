"""Lab 06 - Dining Philosopher Problem using semaphores"""
import threading
import time

N = 5
THINKING, HUNGRY, EATING = 0, 1, 2

state  = [THINKING] * N
mutex  = threading.Semaphore(1)
forks  = [threading.Semaphore(0) for _ in range(N)]


def left(i):  return (i + N - 1) % N
def right(i): return (i + 1) % N


def test(i):
    if state[i] == HUNGRY and state[left(i)] != EATING and state[right(i)] != EATING:
        state[i] = EATING
        print(f"Philosopher {i+1} takes fork {left(i)+1} and {i+1}")
        print(f"Philosopher {i+1} is Eating")
        forks[i].release()


def take_fork(i):
    mutex.acquire()
    state[i] = HUNGRY
    print(f"Philosopher {i+1} is Hungry")
    test(i)
    mutex.release()
    forks[i].acquire()
    time.sleep(0.5)


def put_fork(i):
    mutex.acquire()
    state[i] = THINKING
    print(f"Philosopher {i+1} putting fork {left(i)+1} and {i+1} down")
    print(f"Philosopher {i+1} is Thinking")
    test(left(i))
    test(right(i))
    mutex.release()


def philosopher(i):
    for _ in range(3):   # each philosopher eats 3 times
        time.sleep(0.5)
        take_fork(i)
        time.sleep(0.5)
        put_fork(i)


if __name__ == "__main__":
    print("=== Dining Philosopher Problem (Semaphore) ===\n")
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for i, t in enumerate(threads):
        print(f"Philosopher {i+1} is thinking")
        t.start()
    for t in threads: t.join()
    print("\nAll philosophers finished.")
