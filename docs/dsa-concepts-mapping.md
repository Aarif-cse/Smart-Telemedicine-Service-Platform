# DSA Concepts Mapping

> These are **proposed** applications. None are implemented yet.

| DSA Concept | Possible Application | Time Complexity |
|---|---|---|
| Binary Tree | Hierarchical organization of patient records | O(log n) avg, O(n) worst (search/insert) |
| Binary Search Tree | Ordered storage and quick lookup of patient and doctor records by ID | O(log n) avg, O(n) worst (search/insert/delete) |
| AVL Tree | Balanced searching of patient and doctor records | O(log n) guaranteed (search/insert/delete) |
| Max-Heap / Min-Heap | Priority-based processing of urgent appointments | O(log n) insert/delete, O(1) find min/max |
| Tree Traversal | Systematic processing of patient record information | O(n) |
| Graph | Relationships between patients, doctors and hospitals | O(V + E) for BFS/DFS |
| Adjacency List | Space-efficient connections (sparse graphs) | O(V + E) traversal; O(k) edge lookup |
| Adjacency Matrix | Fast direct-edge lookup (dense graphs) | O(V²) traversal/space; O(1) edge lookup |
