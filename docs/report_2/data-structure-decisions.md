# Data Structure Decisions

This document records which data structure or algorithm is used for each requirement of the Smart Telemedicine Service Platform prototype, and why. All data used is dummy data.

## Summary

| Requirement | Structure / algorithm | File | Time complexity |
|---|---|---|---|
| Patient and doctor records by ID | AVL tree (insert, search, in-order, delete) | `src/avl_tree.py` | O(log n); in-order O(n) |
| Appointments by priority | Binary max-heap (priority queue) | `src/appointment_heap.py` | add/serve O(log n), peek O(1) |
| Patient-doctor-hospital relationships | Graph, adjacency list, BFS, DFS, connected component | `src/graph.py` | O(V + E) |
| Appointments that fit a doctor's limited time | 0/1 knapsack (Dynamic Programming) | `src/dp_scheduling.py` | O(n x W) |
| Sharing consultation slots among doctors | Resource allocation (Dynamic Programming) | `src/dp_scheduling.py` | O(n x R^2) |
| Nearest hospital for a patient | Dijkstra's shortest path | `src/weighted_graph.py` | O((V + E) log V) |

## 1. Records: AVL tree
Records are looked up by ID and listed in sorted order. A plain BST becomes a chain when IDs arrive in increasing order (O(n) search), while an AVL tree rebalances with rotations and keeps its height O(log n). In the program, 15 sorted IDs give height 4 instead of 15. The same class stores patient and doctor records, and deletion handles leaf, one-child and two-children nodes.

## 2. Appointments: max-heap
Emergency appointments must be served first. The heap keeps the highest priority at the root (emergency 3, urgent 2, normal 1); an arrival number makes equal priorities follow booking order. A plain queue would make emergencies wait.

## 3. Relationships: graph with adjacency list
Patients, doctors and hospitals are linked in many-to-many ways. Edges are "consulted" and "works at". An adjacency list needs O(V + E) space because each node has few neighbours; a matrix would need O(V^2). BFS (queue) and DFS (stack) with a visited set find the doctors and hospitals linked to a patient.

## 4. Doctor's time: Dynamic Programming
Choosing which waiting appointments fit into a doctor's available time to get the highest total priority score is a 0/1 knapsack problem. A greedy rule (highest score first) can miss the best set: for 60 minutes it chose one appointment (score 5), while the DP chose two (score 6). Sharing a limited number of consultation slots among doctors is solved with the resource allocation DP.

## 5. Nearest hospital: Dijkstra
Places are nodes and edge weights are distances in km. Dijkstra uses a priority queue (Python's heapq) to always expand the closest unvisited node.

## Limitations
- Data is stored in memory only; there is no database or user interface.
- Only dummy data is used. No real patient data is stored.
- The DP and Dijkstra modules run separately and are not yet part of the booking flow.
- `add_edge` checks for duplicate edges, so it takes O(k) time, where k is the number of neighbours.
- Topics such as spanning trees, Bellman-Ford and Floyd-Warshall are not implemented.
