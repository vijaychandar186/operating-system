"""Lab 07 - Process creation using os.fork(), os.getpid(), os.getppid(), os.wait()"""
import os
import sys
import time

def main():
    print("=== fork() System Call Demo ===\n")

    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)
    elif pid == 0:
        # Child process
        print(f"Child  => PID: {os.getpid()}, PPID: {os.getppid()}")
        print("Child  => Doing some work...")
        time.sleep(1)
        print("Child  => Done. Exiting.")
        sys.exit(0)
    else:
        # Parent process
        print(f"Parent => PID: {os.getpid()}")
        print(f"Parent => Child PID is {pid}. Waiting...")
        child_pid, status = os.wait()
        exit_code = os.WEXITSTATUS(status)
        print(f"Parent => Child (PID {child_pid}) exited with status {exit_code}")
        print("Parent => Child process finished.")


if __name__ == "__main__":
    main()
