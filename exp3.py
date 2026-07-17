import heapq
from colorama import Fore, Style, init
import matplotlib.pyplot as plt
import networkx as nx

init(autoreset=True)


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n, edges):
    """edges: list of (weight, u, v). O(E log E)."""
    edges = sorted(edges)
    uf = UnionFind(n)
    mst, cost = [], 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost


def prim(n, adj, start=0):
    """adj: {u: [(v, w), ...]}. O(E log V) with a heap."""
    INF = float("inf")
    key = [INF] * n
    parent = [-1] * n
    in_mst = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst, cost = [], 0
    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue
        in_mst[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not in_mst[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost


def print_mst(name, mst, cost, color):
    print(color + Style.BRIGHT + f"\n=== {name}'s MST ===")
    for u, v, w in mst:
        print(color + f"  Edge ({u} - {v})  Weight: {w}")
    print(color + Style.BRIGHT + f"  Total MST Cost: {cost}")


def visualize(n, edges, k_mst, p_mst):
    G = nx.Graph()
    for w, u, v in edges:
        G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=7)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, mst, title, mst_color in [
        (axes[0], k_mst, "Kruskal's MST", "#2ecc71"),
        (axes[1], p_mst, "Prim's MST", "#e67e22"),
    ]:
        mst_edges = {(u, v) for u, v, w in mst} | {(v, u) for u, v, w in mst}
        edge_colors = ["#bdc3c7" if (u, v) not in mst_edges else mst_color
                        for u, v in G.edges()]
        edge_widths = [1.2 if (u, v) not in mst_edges else 3.0
                        for u, v in G.edges()]

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#3498db",
                                node_size=550, edgecolors="white")
        nx.draw_networkx_labels(G, pos, ax=ax, font_color="white",
                                 font_weight="bold")
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                                width=edge_widths)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels,
                                      font_size=8)
        ax.set_title(title, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("exp3_mst_visualization.png", dpi=150)
    print(Fore.CYAN + "\nGraph saved as exp3_mst_visualization.png "
          "(gray = original edges, colored = MST edges)")


if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)
    print(Fore.CYAN + Style.BRIGHT + "  EXPERIMENT 3: KRUSKAL'S & PRIM'S MST")
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)

    n = 7
    edges = [
        (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
        (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
        (8, 4, 5), (9, 4, 6), (11, 5, 6),
    ]
    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    k_mst, k_cost = kruskal(n, edges[:])
    p_mst, p_cost = prim(n, adj)

    print_mst("Kruskal", k_mst, k_cost, Fore.GREEN)
    print_mst("Prim", p_mst, p_cost, Fore.YELLOW)

    match = "MATCH" if k_cost == p_cost else "MISMATCH"
    match_color = Fore.GREEN if k_cost == p_cost else Fore.RED
    print(match_color + Style.BRIGHT +
          f"\nVerification: Kruskal cost = {k_cost}, Prim cost = {p_cost} -> {match}")

    visualize(n, edges, k_mst, p_mst)

    print(Fore.CYAN + Style.BRIGHT +
          "\nInference: Kruskal's (O(E log E)) suits sparse graphs since it "
          "sorts edges globally; Prim's (O(E log V) with a heap) suits "
          "dense graphs grown from a start vertex. Both are optimal greedy "
          "solutions and, as verified above, produce the same total weight.")
