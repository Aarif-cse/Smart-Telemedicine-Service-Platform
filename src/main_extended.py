"""Main program for the extra features: AVL deletion, Dynamic Programming and Dijkstra (dummy data only)."""
from avl_tree import AVLTree
from dp_scheduling import knapsack_schedule, greedy_by_score, allocate_slots
from weighted_graph import WeightedGraph


def run_delete():
    print("=== 5. AVL tree: deleting patient records ===")
    tree = AVLTree()
    for pid in range(101, 116):
        tree.insert(pid, {"name": f"Patient {pid}"})
    print("Before : size", tree.size, ", height", tree.height(), ", root", tree.root.key)
    for pid in (108, 101, 115, 999):             # 108 is the root (two children); 999 does not exist
        print(f"Delete {pid}: {'removed' if tree.delete(pid) else 'not found'}")
    print("After  : size", tree.size, ", height", tree.height(), ", root", tree.root.key)
    print("In-order IDs:", [k for k, _ in tree.inorder()])
    print("Search 108  :", tree.search(108))
    print()


def run_knapsack():
    print("=== 6a. Dynamic Programming: 0/1 knapsack (doctor's time) ===")
    waiting = [(101, 45, 5), (102, 30, 3), (103, 30, 3), (104, 30, 2)]   # (patient, minutes, score)
    available = 60
    print(f"Dr. Khan is available for {available} minutes. Waiting appointments (patient, minutes, score):")
    for a in waiting:
        print("  ", a)
    g_total, g_chosen = greedy_by_score(waiting, available)
    d_total, d_chosen = knapsack_schedule(waiting, available)
    print("Greedy (highest score first):", [a[0] for a in g_chosen], "-> total score", g_total)
    print("DP knapsack (best set)      :", [a[0] for a in d_chosen], "-> total score", d_total)
    print()


def run_allocation():
    print("=== 6b. Dynamic Programming: resource allocation (consultation slots) ===")
    benefit = [[0, 6, 10, 12, 13],      # Dr. Khan : benefit for 0, 1, 2, 3, 4 slots
               [0, 5, 9, 12, 14],       # Dr. Rao
               [0, 3, 5, 8, 15]]        # Dr. Mehta
    names = ["Dr. Khan", "Dr. Rao", "Dr. Mehta"]
    total_slots = 4
    best, allocation = allocate_slots(benefit, total_slots)
    print(f"{total_slots} slots shared among 3 doctors:")
    for name, k in zip(names, allocation):
        print(f"  {name}: {k} slot(s)")
    print("Best total benefit:", best)
    print()


def run_dijkstra():
    print("=== 7. Dijkstra: nearest hospital for a patient ===")
    g = WeightedGraph()
    for u, v, km in [("P101", "A", 2), ("P101", "B", 5), ("A", "B", 1),
                     ("A", "H1", 7), ("B", "H1", 4), ("B", "H2", 8), ("H1", "H2", 2)]:
        g.add_edge(u, v, km)
    dist, _ = g.dijkstra("P101")
    print("Distance from P101 (km):", {n: dist[n] for n in ("A", "B", "H1", "H2")})
    hospital, km, path = g.nearest("P101", ["H1", "H2"])
    print(f"Nearest hospital: {hospital} at {km} km via {' -> '.join(path)}")
    print()


if __name__ == "__main__":
    run_delete()
    run_knapsack()
    run_allocation()
    run_dijkstra()
