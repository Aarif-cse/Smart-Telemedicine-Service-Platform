"""Small demo that uses the AVL tree, the heap and the graph together.
Only dummy data is used (no real patient data)."""
from avl_tree import AVLTree
from appointment_heap import AppointmentHeap, EMERGENCY, URGENT, NORMAL, PRIORITY_NAMES
from graph import Graph


def demo_avl():
    print("=== 1. AVL tree: patient records ===")
    tree = AVLTree()
    for pid in range(101, 116):                 # sorted IDs: worst case for a plain BST
        tree.insert(pid, {"name": f"Patient {pid}"})
    print("Patients inserted      :", tree.size)
    print("Tree height            :", tree.height(), "(a plain BST would have height", tree.size, ")")
    print("Rotations performed    :", tree.rotations)
    print("Inorder (sorted) IDs   :", [k for k, _ in tree.inorder()])
    print("Search 107             :", tree.search(107))
    print("Search 999             :", tree.search(999))
    print()


def demo_heap():
    print("=== 2. Heap: appointment priority ===")
    heap = AppointmentHeap()
    bookings = [(101, 201, NORMAL), (102, 202, URGENT), (103, 201, NORMAL),
                (104, 203, EMERGENCY), (105, 202, URGENT), (106, 201, EMERGENCY)]
    print("Booking order:")
    for p, d, pr in bookings:
        heap.add(p, d, pr)
        print(f"  patient {p} -> doctor {d} ({PRIORITY_NAMES[pr]})")
    print("Serving order:")
    while not heap.is_empty():
        a = heap.serve()
        print(f"  patient {a.patient_id} -> doctor {a.doctor_id} ({PRIORITY_NAMES[a.priority]})")
    print()


def build_graph():
    g = Graph()
    for p in ("P101", "P102", "P103"):
        g.add_node(p, "patient")
    for d in ("D201", "D202", "D203"):
        g.add_node(d, "doctor")
    for h in ("H1", "H2"):
        g.add_node(h, "hospital")
    # patient - doctor (consulted)
    for p, d in [("P101", "D201"), ("P101", "D202"), ("P102", "D202"), ("P103", "D203")]:
        g.add_edge(p, d)
    # doctor - hospital (works at)
    for d, h in [("D201", "H1"), ("D202", "H1"), ("D203", "H2")]:
        g.add_edge(d, h)
    return g


def demo_graph():
    print("=== 3. Graph: patient-doctor-hospital relationships ===")
    g = build_graph()
    print("Adjacency list:")
    for node, nbs in g.adj.items():
        print(f"  {node}: {nbs}")
    print("BFS from P101          :", g.bfs("P101"))
    print("DFS from P101          :", g.dfs("P101"))
    print("Doctors linked to P101 :", g.reachable_of_kind("P101", "doctor"))
    print("Hospitals linked to P101:", g.reachable_of_kind("P101", "hospital"))
    print()


def demo_combined():
    print("=== 4. Combined flow: book an appointment ===")
    patients, doctors = AVLTree(), AVLTree()
    for pid, name in [(101, "Asha"), (102, "Ravi"), (103, "Meena")]:
        patients.insert(pid, {"name": name})
    for did, name in [(201, "Dr. Khan"), (202, "Dr. Rao")]:
        doctors.insert(did, {"name": name})
    heap, g = AppointmentHeap(), Graph()

    def book(pid, did, priority):
        p, d = patients.search(pid), doctors.search(did)
        if p is None or d is None:
            print(f"  Booking failed: patient {pid} or doctor {did} not found")
            return
        heap.add(pid, did, priority)
        g.add_node(f"P{pid}", "patient")
        g.add_node(f"D{did}", "doctor")
        g.add_edge(f"P{pid}", f"D{did}")
        print(f"  Booked: {p['name']} with {d['name']} ({PRIORITY_NAMES[priority]})")

    book(101, 201, NORMAL)
    book(102, 202, EMERGENCY)
    book(103, 201, URGENT)
    book(999, 201, NORMAL)           # unknown patient
    print("Next to be served:", heap.peek())
    print("Doctors linked to P101:", g.reachable_of_kind("P101", "doctor"))


if __name__ == "__main__":
    demo_avl()
    demo_heap()
    demo_graph()
    demo_combined()
