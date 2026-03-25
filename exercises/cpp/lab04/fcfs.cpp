#include <iostream>
#include <vector>
using namespace std;

void findWaitingTime(int n, vector<int>& bt, vector<int>& wt) {
    wt[0] = 0;
    for (int i = 1; i < n; i++)
        wt[i] = bt[i-1] + wt[i-1];
}

void findTurnAroundTime(int n, vector<int>& bt, vector<int>& wt, vector<int>& tat) {
    for (int i = 0; i < n; i++)
        tat[i] = bt[i] + wt[i];
}

int main() {
    vector<int> processes = {1, 2, 3};
    vector<int> burst_time = {10, 5, 8};
    int n = processes.size();

    vector<int> wt(n), tat(n);
    findWaitingTime(n, burst_time, wt);
    findTurnAroundTime(n, burst_time, wt, tat);

    int total_wt = 0, total_tat = 0;
    cout << "=== First Come First Serve (FCFS) Scheduling ===\n\n";
    cout << "Process\t\tBurst Time\tWaiting Time\tTurnaround Time\n";
    for (int i = 0; i < n; i++) {
        total_wt  += wt[i];
        total_tat += tat[i];
        cout << "  P" << processes[i] << "\t\t" << burst_time[i]
             << "\t\t" << wt[i] << "\t\t" << tat[i] << "\n";
    }
    cout << "\nAverage Waiting Time    = " << (float)total_wt  / n << "\n";
    cout << "Average Turnaround Time = " << (float)total_tat / n << "\n";
    return 0;
}
