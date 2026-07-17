import heapq
from colorama import Fore, Style, init
import matplotlib.pyplot as plt
import networkx as nx

init(autoreset=True)


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using a min-heap.
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}
    """
    n = len(graph)
    dist = [float("inf")] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path and path[0] == source:
        return path
    return []


def print_table(graph, source, dist, prev):
    print(Fore.CYAN + Style.BRIGHT +
          f"\n{'Vertex':>8} {'Distance':>10} {'Path':>30}")
    print(Fore.CYAN + "-" * 55)
    for v in range(len(graph)):
        path = reconstruct_path(prev, source, v)
        path_str = " -> ".join(map(str, path)) if path else "No path"
        d = dist[v] if dist[v] != float("inf") else "INF"
        color = Fore.GREEN if v != source else Fore.YELLOW
        print(color + f"{v:>8} {str(d):>10} {path_str:>30}")


def visualize(graph, source, dist, prev):
    G = nx.DiGraph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=3)

    tree_edges = set()
    for v, p in enumerate(prev):
        if p is not None:
            tree_edges.add((p, v))

    edge_colors = ["#2ecc71" if (u, v) in tree_edges else "#bdc3c7"
                   for u, v in G.edges()]
    edge_widths = [3.0 if (u, v) in tree_edges else 1.2
                   for u, v in G.edges()]
    node_colors = ["#e74c3c" if node == source else "#3498db"
                   for node in G.nodes()]

    labels = {v: f"{v}\n({dist[v] if dist[v] != float('inf') else 'INF'})"
              for v in G.nodes()}

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700,
                            edgecolors="white")
    nx.draw_networkx_labels(G, pos, labels=labels, font_color="white",
                             font_weight="bold", font_size=9)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths,
                            arrowstyle="-|>", arrowsize=15,
                            connectionstyle="arc3,rad=0.08")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f"Dijkstra Shortest-Path Tree from vertex {source}\n"
              f"(red = source, green = shortest-path tree edges)",
              fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("exp4_dijkstra_visualization.png", dpi=150)
    print(Fore.CYAN + "\nGraph saved as exp4_dijkstra_visualization.png")


if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)
    print(Fore.CYAN + Style.BRIGHT + "  EXPERIMENT 4: DIJKSTRA'S SHORTEST PATH")
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)

    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [(4, 3)],
        4: [(5, 2)],
        5: [],
    }
    source = 0

    dist, prev = dijkstra(graph, source)
    print_table(graph, source, dist, prev)
    visualize(graph, source, dist, prev)

    print(Fore.CYAN + Style.BRIGHT +
          "\nInference: Dijkstra's algorithm, using a min-heap for O((V+E) "
          "log V) performance, correctly computes the shortest distance "
          "and path from the source to every other vertex, making it the "
          "backbone of real-world routing protocols like OSPF.")
