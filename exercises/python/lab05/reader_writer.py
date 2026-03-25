"""Lab 05 - Reader-Writer Problem using threading (monitor-style)"""
import threading
import time


class Monitor:
    def __init__(self):
        self._lock   = threading.Lock()
        self._can_read  = threading.Condition(self._lock)
        self._can_write = threading.Condition(self._lock)
        self.rcnt  = 0  # active readers
        self.wcnt  = 0  # active writers
        self.waitw = 0  # waiting writers

    def begin_read(self, rid):
        with self._can_read:
            while self.wcnt > 0 or self.waitw > 0:
                self._can_read.wait()
            self.rcnt += 1
            print(f"Reader {rid} is reading")

    def end_read(self, rid):
        with self._can_write:
            self.rcnt -= 1
            if self.rcnt == 0:
                self._can_write.notify()

    def begin_write(self, wid):
        with self._can_write:
            self.waitw += 1
            while self.wcnt > 0 or self.rcnt > 0:
                self._can_write.wait()
            self.waitw -= 1
            self.wcnt = 1
            print(f"Writer {wid} is writing")

    def end_write(self, wid):
        with self._can_read:
            self.wcnt = 0
            self._can_read.notify_all()
            self._can_write.notify_all()


monitor = Monitor()


def reader(rid):
    for _ in range(3):
        time.sleep(0.1)
        monitor.begin_read(rid)
        time.sleep(0.05)
        monitor.end_read(rid)


def writer(wid):
    for _ in range(2):
        time.sleep(0.15)
        monitor.begin_write(wid)
        time.sleep(0.05)
        monitor.end_write(wid)


if __name__ == "__main__":
    print("=== Reader-Writer Problem (Monitor) ===\n")
    NUM = 5
    threads = []
    for i in range(1, NUM + 1):
        threads.append(threading.Thread(target=reader, args=(i,)))
        threads.append(threading.Thread(target=writer, args=(i,)))

    for t in threads: t.start()
    for t in threads: t.join()
    print("\nAll readers and writers finished.")
