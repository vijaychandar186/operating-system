"""Lab 13 - Fork + parallel sort: parent uses insertion sort, child uses selection sort"""
import os
import sys
import time


def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a


def selection_sort(arr):
    a = arr[:]
    for i in range(len(a)):
        min_idx = i
        for j in range(i+1, len(a)):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def main():
    print("=== Fork: Parallel Sorting ===\n")
    n = int(input("Enter number of elements: "))
    arr = list(map(int, input(f"Enter {n} elements: ").split()))

    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)
    elif pid == 0:
        time.sleep(0.5)  # let parent print first
        sorted_arr = selection_sort(arr)
        print(f"\nChild  process (PID {os.getpid()}, PPID {os.getppid()}):")
        print(f"Selection Sort result: {sorted_arr}")
    else:
        sorted_arr = insertion_sort(arr)
        print(f"Parent process (PID {os.getpid()}):")
        print(f"Insertion Sort result: {sorted_arr}")
        os.wait()


if __name__ == "__main__":
    main()
