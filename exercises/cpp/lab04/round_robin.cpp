#include <iostream>
#include <vector>
using namespace std;

void findWaitingTime(vector<int>& processes, int n, vector<int>& bt,
                     vector<int>& wt, int quantum) {
    vector<int> rem_bt(bt.begin(), bt.end());
    int t = 0;

    while (true) {
        bool done = true;
        for (int i = 0; i < n; i++) {
            if (rem_bt[i] > 0) {
                done = false;
                if (rem_bt[i] > quantum) {
                    t += quantum;
                    rem_bt[i] -= quantum;
                } else {
                    t += rem_bt[i];
                    wt[i] = t - bt[i];
                    rem_bt[i] = 0;
                }
            }
        }
        if (done) break;
    }
}

void findTurnAroundTime(int n, vector<int>& bt, vector<int>& wt, vector<int>& tat) {
    for (int i = 0; i < n; i++)
        tat[i] = bt[i] + wt[i];
}

void findAvgTime(vector<int>& processes, int n, vector<int>& bt, int quantum) {
    vector<int> wt(n, 0), tat(n, 0);
    findWaitingTime(processes, n, bt, wt, quantum);
    findTurnAroundTime(n, bt, wt, tat);

    int total_wt = 0, total_tat = 0;
    cout << "Process\t\tBurst Time\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        total_wt  += wt[i];
        total_tat += tat[i];
        cout << "  P" << processes[i] << "\t\t" << bt[i]
             << "\t\t" << wt[i] << "\t\t" << tat[i] << "\n";
    }
    cout << "\nAverage Waiting Time    = " << (float)total_wt  / n << "\n";
    cout << "Average Turnaround Time = " << (float)total_tat / n << "\n";
}

int main() {
    vector<int> processes = {1, 2, 3};
    vector<int> burst_time = {10, 5, 8};
    int quantum = 2;
    int n = processes.size();

    cout << "=== Round Robin Scheduling (Quantum = " << quantum << ") ===\n\n";
    findAvgTime(processes, n, burst_time, quantum);
    return 0;
}
