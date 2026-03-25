"""Lab 09 - Message Queue IPC (Reader) using queue + file"""
import pickle
import os

QUEUE_FILE = "/tmp/os_lab09_msgqueue"


def main():
    if not os.path.exists(QUEUE_FILE):
        print("No message queue found. Run msg_writer.py first.")
        return

    with open(QUEUE_FILE, "rb") as f:
        messages = pickle.load(f)

    if not messages:
        print("Message queue is empty.")
        return

    # Receive the first type-1 message
    msg = None
    for i, m in enumerate(messages):
        if m["type"] == 1:
            msg = messages.pop(i)
            break

    if msg is None:
        print("No type-1 message found.")
        return

    # Save remaining messages back
    if messages:
        with open(QUEUE_FILE, "wb") as f:
            pickle.dump(messages, f)
    else:
        os.remove(QUEUE_FILE)
        print("Message queue destroyed.")

    print(f'Message received: "{msg["text"]}"')


if __name__ == "__main__":
    main()
