"""Weighted graph and Dijkstra's shortest path (Unit 2).

Used to find the nearest hospital for a patient: nodes are places, edge weights are
distances in km. Dijkstra needs a priority queue, so Python's heapq module is used.
"""
import heapq


class WeightedGraph:
    def __init__(self):
        self.adj = {}                      # node -> list of (neighbour, distance)

    def add_edge(self, u, v, distance):
        if distance < 0:
            raise ValueError("Dijkstra needs non-negative distances")
        self.adj.setdefault(u, []).append((v, distance))
        self.adj.setdefault(v, []).append((u, distance))

    def dijkstra(self, source):
        """Shortest distance from source to every node. O((V + E) log V)."""
        dist = {node: float("inf") for node in self.adj}
        prev = {node: None for node in self.adj}
        dist[source] = 0
        queue = [(0, source)]              # (distance so far, node), smallest first
        while queue:
            d, node = heapq.heappop(queue)
            if d > dist[node]:
                continue                   # outdated entry, a shorter path was already found
            for neighbour, w in self.adj[node]:
                if d + w < dist[neighbour]:
                    dist[neighbour] = d + w
                    prev[neighbour] = node
                    heapq.heappush(queue, (d + w, neighbour))
        return dist, prev

    def shortest_path(self, source, target):
        """Returns (distance, path as a list of nodes); (inf, []) if not reachable."""
        dist, prev = self.dijkstra(source)
        if dist[target] == float("inf"):
            return float("inf"), []
        path, node = [], target
        while node is not None:
            path.append(node)
            node = prev[node]
        return dist[target], path[::-1]

    def nearest(self, source, targets):
        """The closest of the target nodes (for example hospitals). Returns (target, distance, path)."""
        dist, _ = self.dijkstra(source)
        best = min(targets, key=lambda t: dist[t])
        d, path = self.shortest_path(source, best)
        return best, d, path
