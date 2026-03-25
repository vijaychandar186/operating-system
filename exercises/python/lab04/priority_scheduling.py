"""Lab 04B - Priority Scheduling"""

def priority_scheduling():
    print("=== Priority Scheduling ===\n")
    n = int(input("Enter total number of processes: "))

    procs = []
    print("\nEnter Burst Time and Priority for each process:")
    for i in range(n):
        burst    = int(input(f"P[{i+1}] Burst Time: "))
        priority = int(input(f"P[{i+1}] Priority:   "))
        procs.append({"id": i+1, "burst": burst, "priority": priority})

    # Sort by priority (lower = higher priority)
    procs.sort(key=lambda p: p["priority"])

    # Compute waiting times
    procs[0]["waiting"] = 0
    for i in range(1, n):
        procs[i]["waiting"] = procs[i-1]["waiting"] + procs[i-1]["burst"]

    print(f"\n{'Process':<10}{'Burst':^10}{'Priority':^12}{'Waiting':^12}{'Turnaround'}")
    total_wt = total_tat = 0
    for p in procs:
        p["tat"] = p["burst"] + p["waiting"]
        total_wt  += p["waiting"]
        total_tat += p["tat"]
        print(f"P[{p['id']}]{'':<6}{p['burst']:^10}{p['priority']:^12}{p['waiting']:^12}{p['tat']}")

    print(f"\nAverage Waiting Time    = {total_wt/n:.2f}")
    print(f"Average Turnaround Time = {total_tat/n:.2f}")


if __name__ == "__main__":
    priority_scheduling()
