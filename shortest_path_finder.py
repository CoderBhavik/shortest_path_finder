"""
SHORTEST PATH FINDER
Data Structures Mini Project
Team: Bhavik Suthar, Karan Shah, Kush Posia
Semester 3 | Department: AI and Data Science

Data structures used:
    - Adjacency list (dict of lists) to store the weighted graph
    - Dictionary for distances and parent (predecessor) values
    - Priority queue (min-heap via heapq) for Dijkstra's algorithm

Modules (as in the project presentation):
    1. Graph Creation        -> class Graph
    2. Input Module          -> get_vertex(), menu functions
    3. Shortest-Path Engine  -> Graph.dijkstra()
    4. Path Reconstruction   -> Graph.reconstruct_path()
    5. Result Display        -> display_result(), display_distance_table()
"""

import heapq

INF = float("inf")

class Graph:

    def __init__(self, directed=False):
        self.directed = directed
        # vertex -> list of (neighbour, weight)
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
            return True
        return False

    def add_edge(self, u, v, weight):
        if weight < 0:
            raise ValueError("Dijkstra's algorithm needs non-negative weights.")
        self.add_vertex(u)
        self.add_vertex(v)
        self._set_edge(u, v, weight)
        if not self.directed:
            self._set_edge(v, u, weight)

    def _set_edge(self, u, v, weight):
        
        for i, (nbr, _) in enumerate(self.adj[u]):
            if nbr == v:
                self.adj[u][i] = (v, weight)
                return
        self.adj[u].append((v, weight))

    def vertices(self):
        return sorted(self.adj)

    def edges(self):
        
        seen, out = set(), []
        for u in self.adj:
            for v, w in self.adj[u]:
                if not self.directed:
                    key = frozenset((u, v))
                    if key in seen:
                        continue
                    seen.add(key)
                out.append((u, v, w))
        return sorted(out)

    def dijkstra(self, source):

        dist = {v: INF for v in self.adj}     
        parent = {v: None for v in self.adj}
        dist[source] = 0

        pq = [(0, source)]                    
        while pq:                             
            d, u = heapq.heappop(pq)
            if d > dist[u]:                   
                continue
            for v, w in self.adj[u]:        
                candidate = d + w
                if candidate < dist[v]:      
                    dist[v] = candidate
                    parent[v] = u
                    heapq.heappush(pq, (candidate, v))
        return dist, parent

    @staticmethod
    def reconstruct_path(parent, source, target):
        
        path, node = [], target
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path if path and path[0] == source else []



def display_graph(graph):
    print("\n--- Graph (Adjacency List) ---")
    if not graph.adj:
        print("Graph is empty.")
        return
    for v in graph.vertices():
        nbrs = ", ".join(f"{n}({w:g})" for n, w in sorted(graph.adj[v]))
        print(f"  {v} -> {nbrs if nbrs else '-'}")


def display_result(graph, source, target):
    dist, parent = graph.dijkstra(source)
    path = Graph.reconstruct_path(parent, source, target)
    print("\n--- Shortest Path Result ---")
    if not path:
        print(f"No route exists from {source} to {target}.")
        return
    print(f"Source      : {source}")
    print(f"Destination : {target}")
    print(f"Route       : {' -> '.join(path)}")
    print(f"Total cost  : {dist[target]:g}")
    if len(path) > 1:
        print("Step by step:")
        lookup = {v: w for v, w in graph.adj[path[0]]}
        for a, b in zip(path, path[1:]):
            w = dict(graph.adj[a])[b]
            print(f"  {a} -> {b}  (cost {w:g})")


def display_distance_table(graph, source):
    dist, parent = graph.dijkstra(source)
    print(f"\n--- Distance Table from {source} ---")
    print(f"{'Vertex':<10}{'Distance':<12}Route")
    print("-" * 40)
    for v in graph.vertices():
        if dist[v] == INF:
            print(f"{v:<10}{'unreachable':<12}-")
        else:
            route = " -> ".join(Graph.reconstruct_path(parent, source, v))
            print(f"{v:<10}{dist[v]:<12g}{route}")


def get_vertex(graph, prompt):

    while True:
        name = input(prompt).strip().upper()
        if not name:
            return None
        if name in graph.adj:
            return name
        print(f"  '{name}' is not in the graph. Available: {', '.join(graph.vertices())}")


def get_weight(prompt):
    while True:
        try:
            w = float(input(prompt))
            if w < 0:
                print("  Weight must be non-negative.")
                continue
            return w
        except ValueError:
            print("  Please enter a number.")


def load_sample_graph():

    g = Graph()
    for u, v, w in [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3),
    ]:
        g.add_edge(u, v, w)
    return g


def menu_add_edge(graph):
    u = input("First location name: ").strip().upper()
    v = input("Second location name: ").strip().upper()
    if not u or not v:
        print("Names cannot be empty.")
        return
    if u == v:
        print("A location cannot connect to itself.")
        return
    w = get_weight("Distance / cost: ")
    graph.add_edge(u, v, w)
    print(f"Added connection {u} - {v} with cost {w:g}.")


def menu_find_path(graph):
    if len(graph.adj) < 2:
        print("Add at least two locations first.")
        return
    print(f"Available locations: {', '.join(graph.vertices())}")
    src = get_vertex(graph, "Source (blank to cancel): ")
    if src is None:
        return
    dst = get_vertex(graph, "Destination (blank to cancel): ")
    if dst is None:
        return
    display_result(graph, src, dst)


def menu_distance_table(graph):
    if not graph.adj:
        print("Graph is empty.")
        return
    print(f"Available locations: {', '.join(graph.vertices())}")
    src = get_vertex(graph, "Source (blank to cancel): ")
    if src is not None:
        display_distance_table(graph, src)


def main():
    graph = load_sample_graph()
    print("=" * 50)
    print("        SHORTEST PATH FINDER")
    print("   Data Structures Mini Project")
    print("=" * 50)
    print("A sample graph (A-F) has been loaded.")

    while True:
        print("1. Show graph")
        print("2. Find shortest path")
        print("3. Show distance table from a source")
        print("4. Add a connection (edge)")
        print("5. Reset to sample graph")
        print("6. Start with an empty graph")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            display_graph(graph)
        elif choice == "2":
            menu_find_path(graph)
        elif choice == "3":
            menu_distance_table(graph)
        elif choice == "4":
            menu_add_edge(graph)
        elif choice == "5":
            graph = load_sample_graph()
            print("Sample graph restored.")
        elif choice == "6":
            graph = Graph()
            print("Graph cleared. Use option 4 to add connections.")
        elif choice == "0":
            print("Thank you for using Shortest Path Finder!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
