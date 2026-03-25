"""Lab 04A - Round Robin Scheduling"""

def round_robin(processes, burst_times, quantum):
    n = len(processes)
    rem_bt = burst_times[:]
    wt = [0] * n
    t = 0

    while True:
        done = True
        for i in range(n):
            if rem_bt[i] > 0:
                done = False
                if rem_bt[i] > quantum:
                    t += quantum
                    rem_bt[i] -= quantum
                else:
                    t += rem_bt[i]
                    wt[i] = t - burst_times[i]
                    rem_bt[i] = 0
        if done:
            break

    tat = [burst_times[i] + wt[i] for i in range(n)]

    print("=== Round Robin Scheduling (Quantum =", quantum, ") ===\n")
    print(f"{'Process':<12}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time'}")
    for i in range(n):
        print(f"  P{processes[i]:<10}{burst_times[i]:<15}{wt[i]:<15}{tat[i]}")

    print(f"\nAverage Waiting Time    = {sum(wt)/n:.2f}")
    print(f"Average Turnaround Time = {sum(tat)/n:.2f}")


if __name__ == "__main__":
    processes   = [1, 2, 3]
    burst_times = [10, 5, 8]
    quantum     = 2
    round_robin(processes, burst_times, quantum)
