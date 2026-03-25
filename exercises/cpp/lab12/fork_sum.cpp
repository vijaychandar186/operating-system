// Lab 12 - Child computes sum of odd numbers, Parent computes sum of even numbers
#include <iostream>
#include <sys/wait.h>
#include <unistd.h>
using namespace std;

int main() {
    int a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int n = sizeof(a) / sizeof(a[0]);

    printf("=== Fork: Even/Odd Sum ===\n\n");

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid > 0) {
        // Parent: sum even numbers
        int sumEven = 0;
        for (int i = 0; i < n; i++)
            if (a[i] % 2 == 0) sumEven += a[i];
        cout << "Parent process => Sum of even numbers (1-10): " << sumEven << "\n";
        wait(NULL);
    } else {
        // Child: sum odd numbers
        int sumOdd = 0;
        for (int i = 0; i < n; i++)
            if (a[i] % 2 != 0) sumOdd += a[i];
        cout << "Child  process => Sum of odd numbers  (1-10): " << sumOdd  << "\n";
    }

    return 0;
}
