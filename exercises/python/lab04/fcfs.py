"""Lab 04C - First Come First Serve (FCFS) Scheduling"""

def fcfs(processes, burst_times):
    n = len(processes)
    wt  = [0] * n
    tat = [0] * n

    for i in range(1, n):
        wt[i] = wt[i-1] + burst_times[i-1]
    for i in range(n):
        tat[i] = burst_times[i] + wt[i]

    print("=== First Come First Serve (FCFS) Scheduling ===\n")
    print(f"{'Process':<12}{'Burst Time':<15}{'Waiting Time':<15}{'Turnaround Time'}")
    for i in range(n):
        print(f"  P{processes[i]:<10}{burst_times[i]:<15}{wt[i]:<15}{tat[i]}")

    print(f"\nAverage Waiting Time    = {sum(wt)/n:.2f}")
    print(f"Average Turnaround Time = {sum(tat)/n:.2f}")


if __name__ == "__main__":
    processes   = [1, 2, 3]
    burst_times = [10, 5, 8]
    fcfs(processes, burst_times)
