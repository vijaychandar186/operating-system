# Operating Systems Lab

A complete Operating Systems Lab course with 15 experiments implemented in C++ and Python.

---

## Lab Overview

| Lab | Topic | Type |
|---|---|---|
| 01 | Installing Linux in VM / Linux Boot Process | Theory |
| 02 | Linux Commands – Simple & Advanced | Theory |
| 03 | Shell Scripting | Shell Script |
| 04A | Round Robin Scheduling | C++ / Python |
| 04B | Priority Scheduling | C++ / Python |
| 04C | First Come First Serve (FCFS) | C++ / Python |
| 05 | Reader-Writer Problem (pthread monitors) | C++ / Python |
| 06 | Dining Philosopher Problem (semaphores) | C++ / Python |
| 07 | Process Creation – `fork()`, `getpid()`, `wait()` | C++ / Python |
| 08 | Shared Memory IPC | C++ / Python |
| 09 | Message Queue IPC | C++ / Python |
| 10 | Unidirectional Pipe IPC | C++ / Python |
| 11 | Process Overlay – `execl()` | C++ / Python |
| 12 | Fork: Even/Odd Sum | C++ / Python |
| 13 | Fork: Parallel Sorting | C++ / Python |
| 14 | Shell Code Analysis | Theory |
| 15 | File Permissions & Binary Analysis | Theory |

---

## Running C++ Labs

```bash
# Single-file labs
g++ -o output exercises/cpp/lab04/round_robin.cpp && ./output

# Labs requiring pthreads / semaphores
g++ -o output exercises/cpp/lab05/reader_writer.cpp     -lpthread && ./output
g++ -o output exercises/cpp/lab06/dining_philosopher.cpp -lpthread && ./output

# Lab 11 – build all three programs first
g++ -o hello   exercises/cpp/lab11/hello.cpp
g++ -o loop    exercises/cpp/lab11/loop.cpp
g++ -o overlay exercises/cpp/lab11/overlay.cpp
./overlay

# IPC labs (Linux only)
g++ -o shm_writer exercises/cpp/lab08/shm_writer.cpp && ./shm_writer
g++ -o shm_reader exercises/cpp/lab08/shm_reader.cpp && ./shm_reader

g++ -o msg_writer exercises/cpp/lab09/msg_writer.cpp && ./msg_writer
g++ -o msg_reader exercises/cpp/lab09/msg_reader.cpp && ./msg_reader
```

## Running Python Labs

```bash
python3 exercises/python/lab04/round_robin.py
python3 exercises/python/lab05/reader_writer.py
python3 exercises/python/lab07/fork_demo.py

# IPC labs
python3 exercises/python/lab08/shm_writer.py
python3 exercises/python/lab08/shm_reader.py

python3 exercises/python/lab09/msg_writer.py
python3 exercises/python/lab09/msg_reader.py
```

## Running Shell Scripts

```bash
chmod +x exercises/cpp/lab03/examples.sh
./exercises/cpp/lab03/examples.sh
```

---

## Prerequisites

- **C++17** compiler (`g++ 7+`)
- **Python 3.8+**
- **pthreads** – included on Linux by default
- **POSIX IPC** – Linux kernel 2.6+ (`sys/shm.h`, `sys/msg.h`)
- **bc** – for floating-point in shell scripts (`sudo apt install bc`)
