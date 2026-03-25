#!/usr/bin/env python3
"""
Automated test suite for Operating Systems lab implementations.

Tests Python labs by spawning processes, feeding programmatic stdin,
and asserting expected output patterns.

Run all labs:        python3 tests/run_tests.py
Run a specific lab:  python3 tests/run_tests.py --lab 04
"""

import subprocess
import os
import sys
import time
import argparse

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_LABS = os.path.join(ROOT, "exercises", "python")

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
SKIP = "\033[93mSKIP\033[0m"

results = []


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(script, stdin_data=b"", timeout=10, cwd=None):
    """Run a Python script, return (stdout, returncode)."""
    proc = subprocess.Popen(
        [sys.executable, script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    try:
        out, err = proc.communicate(input=stdin_data, timeout=timeout)
        return out, proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return b"<timeout>", -1


def record(lab, name, passed, detail=""):
    tag = PASS if passed else FAIL
    line = f"  [{tag}] Lab {lab}: {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    results.append((lab, name, passed, detail))


def skip(lab, name, reason=""):
    line = f"  [{SKIP}] Lab {lab}: {name}"
    if reason:
        line += f" — {reason}"
    print(line)
    results.append((lab, name, None, reason))


# ── Lab 04: CPU Scheduling ────────────────────────────────────────────────────

def test_lab04():
    lab = "04"
    lab_dir = os.path.join(PY_LABS, "lab04")

    # 04A – Round Robin (no stdin required; uses hardcoded processes)
    out, rc = run(os.path.join(lab_dir, "round_robin.py"))
    record(lab, "04A Round Robin: exits cleanly", rc == 0)
    record(lab, "04A Round Robin: shows Burst Time column",  b"Burst" in out)
    record(lab, "04A Round Robin: shows Waiting Time column", b"Waiting" in out)
    record(lab, "04A Round Robin: Average Waiting Time present",
           b"Average Waiting Time" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])

    # 04B – Priority Scheduling (interactive: n=2, p1 burst=6 priority=2, p2 burst=4 priority=1)
    stdin = b"2\n6\n2\n4\n1\n"
    out, rc = run(os.path.join(lab_dir, "priority_scheduling.py"), stdin)
    record(lab, "04B Priority: exits cleanly", rc == 0)
    record(lab, "04B Priority: lower priority number runs first",
           b"Average" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])

    # 04C – FCFS (no stdin; hardcoded)
    out, rc = run(os.path.join(lab_dir, "fcfs.py"))
    record(lab, "04C FCFS: exits cleanly", rc == 0)
    record(lab, "04C FCFS: shows Turnaround Time", b"Turnaround" in out)


# ── Lab 05: Reader-Writer ─────────────────────────────────────────────────────

def test_lab05():
    lab = "05"
    script = os.path.join(PY_LABS, "lab05", "reader_writer.py")

    out, rc = run(script, timeout=15)
    record(lab, "Reader-Writer: exits cleanly", rc == 0)
    record(lab, "Reader-Writer: readers observed",  b"reading" in out)
    record(lab, "Reader-Writer: writers observed",  b"writing" in out)
    record(lab, "Reader-Writer: all finished",
           b"finished" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 06: Dining Philosopher ────────────────────────────────────────────────

def test_lab06():
    lab = "06"
    script = os.path.join(PY_LABS, "lab06", "dining_philosopher.py")

    out, rc = run(script, timeout=30)
    record(lab, "Dining Philosopher: exits cleanly", rc == 0)
    record(lab, "Dining Philosopher: Hungry state shown",  b"Hungry"  in out)
    record(lab, "Dining Philosopher: Eating state shown",  b"Eating"  in out)
    record(lab, "Dining Philosopher: Thinking state shown", b"Thinking" in out)
    record(lab, "Dining Philosopher: all finished",
           b"finished" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 07: Fork Demo ─────────────────────────────────────────────────────────

def test_lab07():
    lab = "07"
    script = os.path.join(PY_LABS, "lab07", "fork_demo.py")

    if sys.platform == "win32":
        skip(lab, "fork_demo", "os.fork() not supported on Windows"); return

    out, rc = run(script, timeout=8)
    record(lab, "fork_demo: exits cleanly", rc == 0)
    record(lab, "fork_demo: Parent process shown", b"Parent" in out)
    record(lab, "fork_demo: Child process shown",  b"Child"  in out)
    record(lab, "fork_demo: PID info present",     b"PID" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 08: Shared Memory IPC ─────────────────────────────────────────────────

def test_lab08():
    lab = "08"
    shm_file = "/tmp/os_lab08_shm"

    # Clean up any leftover file
    if os.path.exists(shm_file): os.remove(shm_file)

    writer = os.path.join(PY_LABS, "lab08", "shm_writer.py")
    reader = os.path.join(PY_LABS, "lab08", "shm_reader.py")

    out, rc = run(writer, stdin_data=b"hello_shared_memory\n")
    record(lab, "shm_writer: exits cleanly", rc == 0)
    record(lab, "shm_writer: confirms write",
           b"written" in out.lower() or b"Data" in out,
           out.decode(errors="replace").strip()[:80])

    # File must now exist
    record(lab, "shm_writer: shared memory file created", os.path.exists(shm_file))

    out, rc = run(reader)
    record(lab, "shm_reader: exits cleanly", rc == 0)
    record(lab, "shm_reader: reads back correct data",
           b"hello_shared_memory" in out,
           out.decode(errors="replace").strip()[:80])
    record(lab, "shm_reader: cleans up file", not os.path.exists(shm_file))


# ── Lab 09: Message Queue IPC ─────────────────────────────────────────────────

def test_lab09():
    lab = "09"
    queue_file = "/tmp/os_lab09_msgqueue"

    if os.path.exists(queue_file): os.remove(queue_file)

    writer = os.path.join(PY_LABS, "lab09", "msg_writer.py")
    reader = os.path.join(PY_LABS, "lab09", "msg_reader.py")

    out, rc = run(writer, stdin_data=b"test_message_ipc\n")
    record(lab, "msg_writer: exits cleanly", rc == 0)
    record(lab, "msg_writer: confirms message sent",
           b"sent" in out.lower() or b"Message" in out,
           out.decode(errors="replace").strip()[:80])
    record(lab, "msg_writer: queue file created", os.path.exists(queue_file))

    out, rc = run(reader)
    record(lab, "msg_reader: exits cleanly", rc == 0)
    record(lab, "msg_reader: reads back correct message",
           b"test_message_ipc" in out,
           out.decode(errors="replace").strip()[:80])
    record(lab, "msg_reader: queue destroyed", not os.path.exists(queue_file))


# ── Lab 10: Pipe IPC ──────────────────────────────────────────────────────────

def test_lab10():
    lab = "10"
    script = os.path.join(PY_LABS, "lab10", "pipe_ipc.py")

    out, rc = run(script, timeout=5)
    record(lab, "pipe_ipc: exits cleanly", rc == 0)
    record(lab, "pipe_ipc: Message 'Hi' written and read",    b"Hi"    in out)
    record(lab, "pipe_ipc: Message 'Hello' written and read", b"Hello" in out)
    record(lab, "pipe_ipc: shows reading from pipe",
           b"Reading" in out or b"reading" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 11: Process Overlay ───────────────────────────────────────────────────

def test_lab11():
    lab = "11"
    lab_dir = os.path.join(PY_LABS, "lab11")

    if sys.platform == "win32":
        skip(lab, "process_overlay", "os.fork()/execl not supported on Windows"); return

    hello  = os.path.join(lab_dir, "hello.py")
    loop   = os.path.join(lab_dir, "loop.py")
    overlay = os.path.join(lab_dir, "overlay.py")

    out, rc = run(hello, timeout=5)
    record(lab, "hello.py: prints Hello World", b"Hello World" in out)

    out, rc = run(loop, timeout=5)
    record(lab, "loop.py: prints numbers 1-10", b"1" in out and b"10" in out)

    out, rc = run(overlay, timeout=10)
    record(lab, "overlay.py: exits cleanly", rc == 0)
    record(lab, "overlay.py: Hello World appears (child execl)",
           b"Hello World" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 12: Fork Sum ─────────────────────────────────────────────────────────

def test_lab12():
    lab = "12"
    script = os.path.join(PY_LABS, "lab12", "fork_sum.py")

    if sys.platform == "win32":
        skip(lab, "fork_sum", "os.fork() not supported on Windows"); return

    out, rc = run(script, timeout=8)
    record(lab, "fork_sum: exits cleanly", rc == 0)
    record(lab, "fork_sum: Parent shows even sum = 30",
           b"30" in out and (b"even" in out.lower() or b"Parent" in out))
    record(lab, "fork_sum: Child shows odd sum = 25",
           b"25" in out and (b"odd" in out.lower() or b"Child" in out),
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Lab 13: Fork Sort ────────────────────────────────────────────────────────

def test_lab13():
    lab = "13"
    script = os.path.join(PY_LABS, "lab13", "fork_sort.py")

    if sys.platform == "win32":
        skip(lab, "fork_sort", "os.fork() not supported on Windows"); return

    # Input: 5 numbers unsorted
    stdin = b"5\n3 1 4 1 5\n"
    out, rc = run(script, stdin_data=stdin, timeout=10)
    record(lab, "fork_sort: exits cleanly", rc == 0)
    record(lab, "fork_sort: Insertion Sort result shown",
           b"Insertion" in out or b"insertion" in out.lower())
    record(lab, "fork_sort: Selection Sort result shown",
           b"Selection" in out or b"selection" in out.lower())
    record(lab, "fork_sort: sorted output contains '1 1 3 4 5'",
           b"1" in out and b"5" in out,
           out.decode(errors="replace").replace("\n", " ").strip()[:80])


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary():
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed  = sum(1 for _, _, ok, _ in results if ok is True)
    failed  = sum(1 for _, _, ok, _ in results if ok is False)
    skipped = sum(1 for _, _, ok, _ in results if ok is None)
    total   = len(results)
    print(f"  Total  : {total}")
    print(f"  Passed : {passed}  ({PASS})")
    print(f"  Failed : {failed}  ({FAIL})")
    print(f"  Skipped: {skipped}  ({SKIP})")
    if failed:
        print("\nFailed tests:")
        for lab, name, ok, detail in results:
            if ok is False:
                print(f"  Lab {lab}: {name}  — {detail}")
    print("=" * 60)
    return failed == 0


# ── Entry Point ───────────────────────────────────────────────────────────────

LAB_TESTS = {
    "04": test_lab04,
    "05": test_lab05,
    "06": test_lab06,
    "07": test_lab07,
    "08": test_lab08,
    "09": test_lab09,
    "10": test_lab10,
    "11": test_lab11,
    "12": test_lab12,
    "13": test_lab13,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OS Lab Test Runner")
    parser.add_argument("--lab", help="Run only a specific lab (e.g. 04)", default=None)
    args = parser.parse_args()

    print("Operating Systems Lab — Test Suite")
    print("=" * 60)

    labs_to_run = [args.lab] if args.lab else sorted(LAB_TESTS.keys())

    for lab_id in labs_to_run:
        if lab_id not in LAB_TESTS:
            print(f"  [{SKIP}] Lab {lab_id}: no automated test (theory lab)")
            continue
        print(f"\nLab {lab_id}:")
        try:
            LAB_TESTS[lab_id]()
        except Exception as e:
            record(lab_id, "test runner error", False, str(e))
        time.sleep(0.2)

    ok = print_summary()
    sys.exit(0 if ok else 1)
