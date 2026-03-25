"""Lab 08 - Shared Memory IPC (Writer) using mmap + file"""
import mmap
import os
import struct

SHM_FILE = "/tmp/os_lab08_shm"
SHM_SIZE = 1024


def main():
    data = input("Write data to shared memory: ").encode()
    # Pad to SHM_SIZE
    data = data[:SHM_SIZE-4].ljust(SHM_SIZE-4, b'\x00')
    length = len(data.rstrip(b'\x00'))

    with open(SHM_FILE, "wb") as f:
        f.write(struct.pack("I", length))  # 4 bytes for length
        f.write(data)

    print(f'Data written to shared memory: "{data[:length].decode()}"')
    print("Run shm_reader.py to read the data.")


if __name__ == "__main__":
    main()
