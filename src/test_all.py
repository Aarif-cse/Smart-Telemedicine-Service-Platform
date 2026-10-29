"""Automated tests for the telemedicine prototype. Run:  python -m unittest test_all -v"""
import itertools
import random
import unittest

from avl_tree import AVLTree
from appointment_heap import AppointmentHeap, EMERGENCY, URGENT, NORMAL
from graph import Graph
from dp_scheduling import knapsack_schedule, greedy_by_score, allocate_slots
from weighted_graph import WeightedGraph


def check_avl(node):
    """Returns the height of the subtree and asserts that every node is balanced and its height correct."""
    if node is None:
        return 0
    left, right = check_avl(node.left), check_avl(node.right)
    assert abs(left - right) <= 1, "tree is not balanced"
    assert node.height == 1 + max(left, right), "stored height is wrong"
    return node.height


class TestAVLTree(unittest.TestCase):
    def test_insert_search_and_missing(self):
        t = AVLTree()
        for k in (50, 20, 70):
            t.insert(k, f"rec{k}")
        self.assertEqual(t.search(20), "rec20")
        self.assertIsNone(t.search(99))

    def test_sorted_insertion_stays_balanced(self):
        t = AVLTree()
        for k in range(101, 116):
            t.insert(k, None)
        self.assertEqual(t.height(), 4)
        self.assertEqual(t.rotations, 11)
        self.assertEqual([k for k, _ in t.inorder()], list(range(101, 116)))

    def test_single_left_rotation(self):
        t = AVLTree()
        for k in (10, 20, 30):
            t.insert(k, None)
        self.assertEqual((t.root.key, t.root.left.key, t.root.right.key), (20, 10, 30))
        self.assertEqual(t.rotations, 1)

    def test_random_inserts_keep_balance_and_order(self):
        for _ in range(100):
            keys = random.sample(range(1000), random.randint(1, 100))
            t = AVLTree()
            for k in keys:
                t.insert(k, k)
            check_avl(t.root)
            self.assertEqual([k for k, _ in t.inorder()], sorted(keys))

    def test_delete_leaf_one_child_two_children(self):
        t = AVLTree()
        for k in (50, 30, 70, 20, 40, 60, 80, 10):
            t.insert(k, None)
        self.assertTrue(t.delete(10))        # leaf
        self.assertTrue(t.delete(20))        # node that had one child
        self.assertTrue(t.delete(50))        # root with two children
        self.assertEqual([k for k, _ in t.inorder()], [30, 40, 60, 70, 80])
        self.assertEqual(t.size, 5)
        check_avl(t.root)

    def test_delete_missing_key(self):
        t = AVLTree()
        t.insert(1, None)
        self.assertFalse(t.delete(99))
        self.assertEqual(t.size, 1)

    def test_random_deletes_keep_balance(self):
        for _ in range(100):
            keys = random.sample(range(500), random.randint(1, 80))
            t = AVLTree()
            for k in keys:
                t.insert(k, None)
            random.shuffle(keys)
            removed = keys[: len(keys) // 2]
            for k in removed:
                self.assertTrue(t.delete(k))
                check_avl(t.root)
            rest = sorted(set(keys) - set(removed))
            self.assertEqual([k for k, _ in t.inorder()], rest)
            self.assertEqual(t.size, len(rest))


class TestAppointmentHeap(unittest.TestCase):
    def test_priority_then_booking_order(self):
        h = AppointmentHeap()
        bookings = [(101, NORMAL), (102, URGENT), (103, NORMAL), (104, EMERGENCY), (105, URGENT), (106, EMERGENCY)]
        for pid, pr in bookings:
            h.add(pid, 201, pr)
        served = []
        while not h.is_empty():
            served.append(h.serve().patient_id)
        self.assertEqual(served, [104, 106, 102, 105, 101, 103])

    def test_empty_heap(self):
        h = AppointmentHeap()
        self.assertIsNone(h.serve())
        self.assertIsNone(h.peek())

    def test_random_order_matches_sorting(self):
        for _ in range(100):
            items = [(i, random.choice([1, 2, 3])) for i in range(random.randint(1, 60))]
            h = AppointmentHeap()
            for i, pr in items:
                h.add(i, 0, pr)
            out = []
            while not h.is_empty():
                a = h.serve()
                out.append((a.priority, a.patient_id))
            self.assertEqual(out, sorted([(pr, i) for i, pr in items], key=lambda x: (-x[0], x[1])))


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        for p in ("P101", "P102"):
            self.g.add_node(p, "patient")
        for d in ("D201", "D202"):
            self.g.add_node(d, "doctor")
        self.g.add_node("H1", "hospital")
        for u, v in [("P101", "D201"), ("P101", "D202"), ("P102", "D202"), ("D201", "H1"), ("D202", "H1")]:
            self.g.add_edge(u, v)

    def test_bfs_and_dfs_order(self):
        self.assertEqual(self.g.bfs("P101"), ["P101", "D201", "D202", "H1", "P102"])
        self.assertEqual(self.g.dfs("P101"), ["P101", "D201", "H1", "D202", "P102"])

    def test_linked_nodes_by_kind(self):
        self.assertEqual(self.g.reachable_of_kind("P101", "doctor"), ["D201", "D202"])
        self.assertEqual(self.g.reachable_of_kind("P101", "hospital"), ["H1"])

    def test_unknown_node_and_duplicate_edge(self):
        self.assertEqual(self.g.bfs("X"), [])
        with self.assertRaises(ValueError):
            self.g.add_edge("P101", "X")
        self.g.add_edge("P101", "D201")                  # duplicate edge is ignored
        self.assertEqual(self.g.neighbors("P101"), ["D201", "D202"])


def brute_knapsack(items, cap):
    best = 0
    for r in range(len(items) + 1):
        for combo in itertools.combinations(items, r):
            if sum(a[1] for a in combo) <= cap:
                best = max(best, sum(a[2] for a in combo))
    return best


class TestDynamicProgramming(unittest.TestCase):
    def test_knapsack_example_beats_greedy(self):
        items = [(101, 45, 5), (102, 30, 3), (103, 30, 3), (104, 30, 2)]
        total, chosen = knapsack_schedule(items, 60)
        self.assertEqual(total, 6)
        self.assertEqual([a[0] for a in chosen], [102, 103])
        self.assertEqual(greedy_by_score(items, 60)[0], 5)

    def test_knapsack_matches_brute_force(self):
        for _ in range(200):
            items = [(i, random.randint(5, 40), random.randint(1, 9)) for i in range(random.randint(0, 8))]
            cap = random.randint(0, 100)
            total, chosen = knapsack_schedule(items, cap)
            self.assertEqual(total, brute_knapsack(items, cap))
            self.assertLessEqual(sum(a[1] for a in chosen), cap)
            self.assertEqual(sum(a[2] for a in chosen), total)
            self.assertGreaterEqual(total, greedy_by_score(items, cap)[0])

    def test_allocation_matches_brute_force(self):
        for _ in range(100):
            n, slots = random.randint(1, 4), random.randint(0, 6)
            benefit = [[0] + sorted(random.randint(1, 20) for _ in range(slots)) for _ in range(n)]
            best, alloc = allocate_slots(benefit, slots)
            brute = max(sum(benefit[i][k] for i, k in enumerate(a))
                        for a in itertools.product(range(slots + 1), repeat=n) if sum(a) <= slots)
            self.assertEqual(best, brute)
            self.assertLessEqual(sum(alloc), slots)
            self.assertEqual(sum(benefit[i][k] for i, k in enumerate(alloc)), best)


class TestDijkstra(unittest.TestCase):
    def test_nearest_hospital(self):
        g = WeightedGraph()
        for u, v, km in [("P101", "A", 2), ("P101", "B", 5), ("A", "B", 1),
                         ("A", "H1", 7), ("B", "H1", 4), ("B", "H2", 8), ("H1", "H2", 2)]:
            g.add_edge(u, v, km)
        self.assertEqual(g.nearest("P101", ["H1", "H2"]), ("H1", 7, ["P101", "A", "B", "H1"]))
        self.assertEqual(g.shortest_path("P101", "H2")[0], 9)

    def test_matches_floyd_warshall(self):
        for _ in range(100):
            n = random.randint(2, 8)
            g, inf = WeightedGraph(), float("inf")
            d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
            for i in range(n):
                g.adj.setdefault(i, [])
            for _ in range(random.randint(1, 14)):
                u, v, w = random.randrange(n), random.randrange(n), random.randint(1, 9)
                if u != v:
                    g.add_edge(u, v, w)
                    d[u][v] = min(d[u][v], w)
                    d[v][u] = min(d[v][u], w)
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        d[i][j] = min(d[i][j], d[i][k] + d[k][j])
            dist, _ = g.dijkstra(0)
            self.assertEqual([dist[i] for i in range(n)], d[0])

    def test_unreachable_and_negative(self):
        g = WeightedGraph()
        g.add_edge("A", "B", 1)
        g.adj["C"] = []
        self.assertEqual(g.shortest_path("A", "C"), (float("inf"), []))
        with self.assertRaises(ValueError):
            g.add_edge("A", "C", -1)


if __name__ == "__main__":
    unittest.main()
