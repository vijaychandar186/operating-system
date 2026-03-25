#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Process {
    int id, burst, priority, waiting, turnaround;
};

int main() {
    int n;
    cout << "=== Priority Scheduling ===\n";
    cout << "Enter total number of processes: ";
    cin >> n;

    vector<Process> procs(n);
    cout << "\nEnter Burst Time and Priority for each process:\n";
    for (int i = 0; i < n; i++) {
        procs[i].id = i + 1;
        cout << "P[" << i + 1 << "] Burst Time: ";
        cin >> procs[i].burst;
        cout << "P[" << i + 1 << "] Priority:   ";
        cin >> procs[i].priority;
    }

    // Sort by priority (lower number = higher priority)
    sort(procs.begin(), procs.end(), [](const Process& a, const Process& b) {
        return a.priority < b.priority;
    });

    // Calculate waiting times
    procs[0].waiting = 0;
    for (int i = 1; i < n; i++)
        procs[i].waiting = procs[i-1].waiting + procs[i-1].burst;

    int total_wt = 0, total_tat = 0;
    cout << "\nProcess\tBurst Time\tPriority\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        procs[i].turnaround = procs[i].burst + procs[i].waiting;
        total_wt  += procs[i].waiting;
        total_tat += procs[i].turnaround;
        cout << "P[" << procs[i].id << "]\t" << procs[i].burst << "\t\t"
             << procs[i].priority << "\t\t" << procs[i].waiting
             << "\t\t" << procs[i].turnaround << "\n";
    }

    cout << "\nAverage Waiting Time    = " << (float)total_wt  / n << "\n";
    cout << "Average Turnaround Time = " << (float)total_tat / n << "\n";
    return 0;
}
