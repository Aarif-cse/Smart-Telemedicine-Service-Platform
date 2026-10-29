# Smart Telemedicine Service Platform

| | |
|---|---|
| **Course** | Data Structure and Algorithms - II (CCSE0301) |
| **Faculty** | Mr. Shamshad Ali |
| **Student** | Aarif Ansari (Roll No. 2501330100002), B.Tech CSE-A |
| **Type** | Individual PBL Assignment |
| **SDG** | SDG 3 - Good Health and Well-Being |

## About
A prototype for a telemedicine platform that uses Trees, Heaps, Graphs and Dynamic Programming to manage patients, doctors, appointments and their relationships. Only dummy data is used.

## Status
- **Review 1:** Problem understanding and concept study.
- **Review 2:** AVL tree, heap and graph (BFS/DFS) implemented with a demo.
- **Final:** Added AVL deletion, Dynamic Programming (knapsack, resource allocation), Dijkstra, 19 automated tests and a larger-data benchmark.

## What is implemented
| Requirement | Structure / algorithm | File |
|---|---|---|
| Patient and doctor records by ID | AVL tree (insert, search, in-order, delete) | `src/avl_tree.py` |
| Appointments by priority | Max-heap (priority queue) | `src/appointment_heap.py` |
| Patient-doctor-hospital relationships | Graph (adjacency list), BFS, DFS | `src/graph.py` |
| Appointments within a doctor's time; slot sharing | Dynamic Programming | `src/dp_scheduling.py` |
| Nearest hospital | Dijkstra's algorithm | `src/weighted_graph.py` |

## How to run
Requires Python 3. No external libraries are needed.

```bash
cd src
python main.py             # AVL tree, heap, graph and a combined booking flow
python main_extended.py    # AVL deletion, Dynamic Programming and Dijkstra
python avl_rotation.py     # one AVL rotation step by step
python -m unittest test_all -v   # 19 automated tests
python benchmark.py        # larger-data test
```

## Repository contents
- [`src/`](src) - source code, programs and tests
- [`docs/`](docs) - problem statement, concept mapping, [data structure decisions](docs/data-structure-decisions.md), [graph design](docs/graph-design.md)
- [`research/`](research) - research papers referred to
- [`screenshots/`](screenshots) - output screenshots
