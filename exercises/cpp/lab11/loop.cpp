// Lab 11 - loop: prints 1..10 (or 1..n if argv[1] given)
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char* argv[]) {
    int n = 10;
    if (argc > 1) n = atoi(argv[1]);
    for (int i = 1; i <= n; i++)
        printf("%d\t", i);
    printf("\n");
    return 0;
}
