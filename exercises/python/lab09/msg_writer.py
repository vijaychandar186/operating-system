"""Lab 09 - Message Queue IPC (Writer) using queue + file"""
import pickle
import os

QUEUE_FILE = "/tmp/os_lab09_msgqueue"


def main():
    text = input("Write data to message queue: ")
    messages = []

    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "rb") as f:
            messages = pickle.load(f)

    messages.append({"type": 1, "text": text})

    with open(QUEUE_FILE, "wb") as f:
        pickle.dump(messages, f)

    print(f'Message sent: "{text}"')
    print("Run msg_reader.py to receive the message.")


if __name__ == "__main__":
    main()
