# Data Structure Decisions

This document records which data structure is used for each requirement of the Smart Telemedicine Service Platform prototype, and why. All data used is dummy data.

## Summary

| Requirement | Structure | File | Main operations | Time complexity |
|---|---|---|---|---|
| Store and search patient records by Patient ID | AVL tree | `src/avl_tree.py` | insert, search, inorder | O(log n), inorder O(n) |
| Store and search doctor records by Doctor ID | AVL tree (same class) | `src/avl_tree.py` | insert, search, inorder | O(log n), inorder O(n) |
| Serve appointments by priority | Max-heap (priority queue) | `src/appointment_heap.py` | add, serve, peek | O(log n), peek O(1) |
| Patient-doctor-hospital relationships | Graph, adjacency list | `src/graph.py` | add_node, add_edge, BFS, DFS | O(V + E) for BFS/DFS |

## 1. Patient and doctor records: AVL tree

**Why:** Records are looked up by ID, and a listing in sorted order is also needed. A tree keeps the records ordered, so an inorder traversal gives them sorted by ID.

**Why AVL and not a plain BST:** If IDs are inserted in increasing order (common for newly generated IDs), a plain BST turns into a chain and search becomes O(n). An AVL tree rebalances itself with rotations, so its height stays O(log n). In the demo, 15 sorted patient IDs give a tree of height 4 instead of 15.

**Alternatives considered:**
- Plain BST: simple, but can become skewed.
- Sorted array: binary search is fast, but insertion is O(n).
- Hash table: fast lookup, but does not keep records in sorted order.

**Doctor records:** The same AVL tree class is reused with Doctor ID as the key.

## 2. Appointments: max-heap

**Why:** Emergency appointments must be served before urgent and normal ones, regardless of booking order. A heap always keeps the highest-priority appointment at the root.

**Priority levels:** Emergency (3), Urgent (2), Normal (1). Appointments with the same priority are served in booking order, using an arrival number as a tie-breaker.

**Alternatives considered:**
- Plain queue: serves in booking order only, so emergencies would wait.
- Sorted list: serving is easy, but every insertion costs O(n).

## 3. Relationships: graph with adjacency list

**Why:** Patients, doctors, and hospitals are connected in many-to-many ways (one patient consults several doctors, one doctor treats several patients). A graph represents this directly.

**Nodes:** patient (`P101`), doctor (`D201`), hospital (`H1`).
**Edges:** patient-doctor ("consulted") and doctor-hospital ("works at"). Edges are undirected.

**Why adjacency list and not adjacency matrix:** Each patient is linked to only a few doctors, so the graph is sparse. A list needs O(V + E) space, while a matrix needs O(V²).

**Traversals:**
- BFS (queue) visits nodes level by level and is used to find the doctors and hospitals connected to a patient.
- DFS (stack) goes deep first and explores all connected nodes.
- Both use a visited set so that no node is processed twice. Both take O(V + E).

## Current limitations

- Record deletion in the AVL tree is not implemented yet.
- Data is stored in memory only; there is no database.
- Only dummy data is used. No real patient data is stored.
- `add_edge` checks for duplicate edges, so it takes O(k) time, where k is the number of neighbours of the node.
