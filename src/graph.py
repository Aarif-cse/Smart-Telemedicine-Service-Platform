"""Graph of patient-doctor-hospital relationships, stored as an adjacency list.

Nodes are strings such as "P101" (patient), "D201" (doctor), "H1" (hospital).
Edges are undirected, e.g. patient-doctor ("consulted") and doctor-hospital
("works at"). The adjacency list is a dict: node -> list of neighbours.
"""
from collections import deque


class Graph:
    def __init__(self):
        self.adj = {}     # node -> list of neighbouring nodes
        self.kind = {}    # node -> "patient" / "doctor" / "hospital"

    def add_node(self, node, kind):
        if node not in self.adj:
            self.adj[node] = []
            self.kind[node] = kind

    def add_edge(self, u, v):
        """Connect two existing nodes. O(1) (plus a small duplicate check)."""
        if u not in self.adj or v not in self.adj:
            raise ValueError("both nodes must be added before adding an edge")
        if v not in self.adj[u]:
            self.adj[u].append(v)
            self.adj[v].append(u)

    def neighbors(self, node):
        return list(self.adj.get(node, []))

    def bfs(self, start):
        """Breadth-first search: visits nodes level by level using a queue. O(V + E)."""
        if start not in self.adj:
            return []
        visited = {start}
        queue = deque([start])
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for nb in self.adj[node]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return order

    def dfs(self, start):
        """Depth-first search: goes as deep as possible first, using a stack. O(V + E)."""
        if start not in self.adj:
            return []
        visited = set()
        stack = [start]
        order = []
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for nb in reversed(self.adj[node]):   # reversed so the first neighbour is visited first
                if nb not in visited:
                    stack.append(nb)
        return order

    def reachable_of_kind(self, start, kind):
        """All nodes of the given kind connected to start (found using BFS)."""
        return [n for n in self.bfs(start) if n != start and self.kind[n] == kind]
