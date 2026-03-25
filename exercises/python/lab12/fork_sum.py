"""Lab 12 - Child computes sum of odd numbers, Parent computes sum of even numbers"""
import os
import sys

def main():
    print("=== Fork: Even/Odd Sum ===\n")
    numbers = list(range(1, 11))

    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)
    elif pid > 0:
        sum_even = sum(x for x in numbers if x % 2 == 0)
        print(f"Parent process => Sum of even numbers (1-10): {sum_even}")
        os.wait()
    else:
        sum_odd = sum(x for x in numbers if x % 2 != 0)
        print(f"Child  process => Sum of odd numbers  (1-10): {sum_odd}")


if __name__ == "__main__":
    main()
