"""Lab 10 - Unidirectional Pipe IPC using os.pipe()"""
import os

def main():
    print("=== Unidirectional Pipe IPC ===\n")

    r_fd, w_fd = os.pipe()
    messages = ["Hi", "Hello"]

    for msg in messages:
        print(f'Writing to pipe   - Message: "{msg}"')
        os.write(w_fd, msg.encode())
        received = os.read(r_fd, 64).decode()
        print(f'Reading from pipe - Message: "{received}"\n')

    os.close(r_fd)
    os.close(w_fd)


if __name__ == "__main__":
    main()
