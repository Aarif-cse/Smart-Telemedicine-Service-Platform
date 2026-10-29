"""Larger-data test: checks the growth of the data structures against their expected complexities.
Dummy data only. Times depend on the computer; heights and counts do not."""
import math
import random
import time

from avl_tree import AVLTree
from appointment_heap import AppointmentHeap
from graph import Graph

random.seed(42)


def bench_avl():
    print("1. AVL tree: height after n insertions (a plain BST on sorted IDs would have height n)")
    print(f"{'n':>7} {'order':>7} {'height':>7} {'AVL bound':>10} {'rotations':>10} {'time (s)':>9}")
    for n in (100, 1000, 10000):
        for order in ("sorted", "random"):
            ids = list(range(n))
            if order == "random":
                random.shuffle(ids)
            tree, start = AVLTree(), time.perf_counter()
            for k in ids:
                tree.insert(k, None)
            elapsed = time.perf_counter() - start
            bound = 1.4405 * math.log2(n + 2) + 0.672        # worst-case AVL height (counted in nodes)
            assert tree.height() <= bound
            print(f"{n:>7} {order:>7} {tree.height():>7} {bound:>10.1f} {tree.rotations:>10} {elapsed:>9.3f}")
    print()


def bench_heap():
    print("2. Heap: n bookings added, then all served (order checked)")
    print(f"{'n':>7} {'time (s)':>9}  order correct")
    for n in (1000, 10000, 50000):
        heap = AppointmentHeap()
        start = time.perf_counter()
        for i in range(n):
            heap.add(i, 0, random.choice((1, 2, 3)))
        last, ok = None, True
        while not heap.is_empty():
            a = heap.serve()
            key = (-a.priority, a.arrival)
            ok = ok and (last is None or key >= last)
            last = key
        print(f"{n:>7} {time.perf_counter() - start:>9.3f}  {ok}")
        assert ok
    print()


def bench_graph():
    print("3. Graph: BFS and DFS on a sparse graph (V nodes, about 2V edges)")
    print(f"{'V':>7} {'E':>7} {'BFS (s)':>9} {'DFS (s)':>9}  nodes reached")
    for v in (1000, 5000, 20000):
        g = Graph()
        for i in range(v):
            g.add_node(i, "node")
        for i in range(v):
            g.add_edge(i, (i + 1) % v)                       # ring: keeps the graph connected
        for _ in range(v):
            a, b = random.randrange(v), random.randrange(v)
            if a != b:
                g.add_edge(a, b)
        edges = sum(len(x) for x in g.adj.values()) // 2
        s = time.perf_counter(); order = g.bfs(0); t_bfs = time.perf_counter() - s
        s = time.perf_counter(); g.dfs(0); t_dfs = time.perf_counter() - s
        print(f"{v:>7} {edges:>7} {t_bfs:>9.4f} {t_dfs:>9.4f}  {len(order)}")
        assert len(order) == v
    print()


if __name__ == "__main__":
    bench_avl()
    bench_heap()
    bench_graph()
