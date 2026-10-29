"""Dynamic Programming (Unit 3) for the telemedicine platform.

1. 0/1 knapsack: choose which waiting appointments fit into a doctor's available
   time so that the total priority score is as large as possible.
2. Resource allocation: share a limited number of consultation slots among doctors
   so that the total benefit is as large as possible.

An appointment is a tuple (patient_id, minutes, priority_score).
"""


def knapsack_schedule(appointments, available_minutes):
    """0/1 knapsack. Each appointment is taken completely or not at all.
    Returns (best total score, chosen appointments). Time O(n * W), space O(n * W)."""
    n, cap = len(appointments), available_minutes
    # table[i][w] = best score using the first i appointments within w minutes
    table = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, minutes, score = appointments[i - 1]
        for w in range(cap + 1):
            table[i][w] = table[i - 1][w]                         # skip appointment i
            if minutes <= w:                                      # or take it
                table[i][w] = max(table[i][w], table[i - 1][w - minutes] + score)
    chosen, w = [], cap                                           # trace back the choices
    for i in range(n, 0, -1):
        if table[i][w] != table[i - 1][w]:                        # appointment i was taken
            chosen.append(appointments[i - 1])
            w -= appointments[i - 1][1]
    chosen.reverse()
    return table[n][cap], chosen


def greedy_by_score(appointments, available_minutes):
    """Greedy rule (highest score first), used only to compare with the DP answer."""
    chosen, used, total = [], 0, 0
    for appt in sorted(appointments, key=lambda a: (-a[2], a[1])):
        if used + appt[1] <= available_minutes:
            chosen.append(appt)
            used += appt[1]
            total += appt[2]
    return total, chosen


def allocate_slots(benefit, total_slots):
    """Resource allocation: benefit[i][k] = benefit if doctor i receives k slots (k = 0, 1, ...).
    Returns (best total benefit, slots given to each doctor). Time O(n * R^2), R = total slots."""
    n = len(benefit)
    best = [[0] * (total_slots + 1) for _ in range(n + 1)]       # best[i][r]: first i doctors, r slots
    pick = [[0] * (total_slots + 1) for _ in range(n + 1)]       # slots given to doctor i
    for i in range(1, n + 1):
        for r in range(total_slots + 1):
            best[i][r] = None
            for k in range(min(r, len(benefit[i - 1]) - 1) + 1):
                value = best[i - 1][r - k] + benefit[i - 1][k]
                if best[i][r] is None or value > best[i][r]:
                    best[i][r], pick[i][r] = value, k
    allocation, r = [0] * n, total_slots                          # trace back
    for i in range(n, 0, -1):
        allocation[i - 1] = pick[i][r]
        r -= pick[i][r]
    return best[n][total_slots], allocation
