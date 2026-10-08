# Smart Telemedicine Service Platform

| | |
|---|---|
| **Course** | Data Structure and Algorithms - II (CCSE0301) |
| **Faculty** | Mr. Shamshad Ali |
| **Student** | Aarif Ansari (Roll No. 2501330100002), B.Tech CSE-A |
| **Type** | Individual PBL Assignment |
| **SDG** | SDG 3 - Good Health and Well-Being |

## About
A prototype for a telemedicine platform that manages patients, doctors, appointments and their relationships using Trees, Heaps and Graphs. Only dummy data is used.

## Current Status
- **Review 1 (Month 1):** Problem understanding and concept study.
- **Review 2 (Month 2):** Core data structures designed and implemented in Python, with a small demo.
- **Next:** Integration into one flow, record deletion, larger test data and complexity analysis.

## Data Structures Used
| Requirement | Structure | File |
|---|---|---|
| Patient and doctor records by ID | AVL tree | `src/avl_tree.py` |
| Appointments by priority | Max-heap (priority queue) | `src/appointment_heap.py` |
| Patient-doctor-hospital relationships | Graph (adjacency list), BFS, DFS | `src/graph.py` |

## How to Run
Requires Python 3. No external libraries are needed.

```bash
cd src
python demo.py            # AVL tree, heap, graph and a combined booking flow
python rotation_demo.py   # one AVL rotation step by step
```

## Repository Contents
- [`src/`](src) - source code and demos
- [`docs/`](docs) - problem statement, concept mapping, [data structure decisions](docs/report_2/data-structure-decisions.md), [graph design](docs/report_2/graph-design.md)
- [`research/`](research) - research papers referred to
- [`screenshots/`](screenshots) - output screenshots for Review 2
