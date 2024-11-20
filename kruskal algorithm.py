class GraphEdge:
    def __init__(self, weight, start, end):
        self.weight = weight
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start} --({self.weight})--> {self.end}"


class DisjointSetUnion:
    def __init__(self, vertices):
        # Initialize the parent and rank dictionaries
        self.parent = {vertex: vertex for vertex in vertices}
        self.rank = {vertex: 0 for vertex in vertices}

    def find(self, vertex):
        # Path compression to optimize future queries
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, vertex1, vertex2):
        # Union by rank to keep the tree flat
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1


def kruskal_mst(vertices, edges):
    """
    Finds the Minimum Spanning Tree (MST) using Kruskal's algorithm.

    :param vertices: Set of vertices in the graph.
    :param edges: List of GraphEdge objects representing graph edges.
    :return: Tuple containing the MST edges and the total weight of the MST.
    """
    if not vertices or not edges:
        print("Error: The graph must have at least one vertex and one edge.")
        return [], 0

    # Sort edges by weight (ascending order)
    edges = sorted(edges, key=lambda edge: edge.weight)
    dsu = DisjointSetUnion(vertices)
    mst_result = []
    total_weight = 0

    for edge in edges:
        # If the edge doesn't form a cycle, add it to the MST
        if dsu.find(edge.start) != dsu.find(edge.end):
            dsu.union(edge.start, edge.end)
            mst_result.append(edge)
            total_weight += edge.weight

    # Check if all vertices are connected (i.e., the graph is a spanning tree)
    connected_components = set(dsu.find(vertex) for vertex in vertices)
    if len(connected_components) > 1:
        print("\nWarning: The graph is disconnected. MST includes only connected components.")
        print(f"Number of connected components: {len(connected_components)}")
    
    return mst_result, total_weight


if __name__ == "__main__":
    # Define nodes and edges for Kruskal's example
    nodes_kruskal = {"a", "b", "c", "d", "e", "f", "g", "h", "i"}
    edges_kruskal = [
        GraphEdge(4, "a", "b"),
        GraphEdge(8, "a", "h"),
        GraphEdge(8, "b", "c"),
        GraphEdge(11, "b", "h"),
        GraphEdge(7, "c", "d"),
        GraphEdge(4, "c", "f"),
        GraphEdge(2, "c", "i"),
        GraphEdge(6, "c", "g"),
        GraphEdge(9, "d", "e"),
        GraphEdge(14, "d", "f"),
        GraphEdge(10, "e", "f"),
        GraphEdge(2, "f", "g"),
        GraphEdge(1, "g", "h"),
        GraphEdge(7, "h", "i")
    ]

    # Perform Kruskal's MST
    mst, total_weight = kruskal_mst(nodes_kruskal, edges_kruskal)

    # Output results
    if mst:
        print("\nEdges in Kruskal's MST:")
        for edge in mst:
            print(edge)
        print(f"\nTotal weight of MST: {total_weight}")
    else:
        print("No MST could be formed due to insufficient edges or invalid input.")
