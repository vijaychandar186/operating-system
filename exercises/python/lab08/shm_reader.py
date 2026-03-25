"""Lab 08 - Shared Memory IPC (Reader) using mmap + file"""
import struct
import os

SHM_FILE = "/tmp/os_lab08_shm"


def main():
    if not os.path.exists(SHM_FILE):
        print("No shared memory file found. Run shm_writer.py first.")
        return

    with open(SHM_FILE, "rb") as f:
        length = struct.unpack("I", f.read(4))[0]
        data   = f.read(length).decode()

    print(f'Data read from shared memory: "{data}"')
    os.remove(SHM_FILE)
    print("Shared memory file removed.")


if __name__ == "__main__":
    main()
