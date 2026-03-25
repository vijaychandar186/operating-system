"""Lab 11 - Process Overlay using os.execl()"""
import os
import sys
import time

def main():
    print("=== Process Overlay Demo ===\n")

    pid = os.fork()

    if pid < 0:
        print("fork failed", file=sys.stderr)
        sys.exit(1)
    elif pid == 0:
        print("Child  => Running hello.py via execl")
        os.execl(sys.executable, sys.executable, os.path.join(os.path.dirname(__file__), "hello.py"))
        print("This won't print")
    else:
        os.wait()
        print("Parent => Running loop.py via execl")
        os.execl(sys.executable, sys.executable,
                 os.path.join(os.path.dirname(__file__), "loop.py"), "5")
        print("This won't print")


if __name__ == "__main__":
    main()
