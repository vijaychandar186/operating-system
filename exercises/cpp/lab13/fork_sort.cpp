// Lab 13 - Fork + parallel sort: parent uses insertion sort, child uses selection sort
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int temp = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > temp) {
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = temp;
    }
}

void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[min]) min = j;
        int tmp = arr[i]; arr[i] = arr[min]; arr[min] = tmp;
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int n;
    printf("=== Fork: Parallel Sorting ===\n\n");
    printf("Enter number of elements: ");
    scanf("%d", &n);

    int arr[30];
    printf("Enter %d elements: ", n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    // Copy for child
    int arr2[30];
    for (int i = 0; i < n; i++) arr2[i] = arr[i];

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child: selection sort
        sleep(1); // let parent print first
        printf("\nChild  process (PID %d, PPID %d):\n", getpid(), getppid());
        selectionSort(arr2, n);
        printf("Selection Sort result: ");
        printArray(arr2, n);
    } else {
        // Parent: insertion sort
        printf("Parent process (PID %d):\n", getpid());
        insertionSort(arr, n);
        printf("Insertion Sort result: ");
        printArray(arr, n);
        wait(NULL);
    }

    return 0;
}
