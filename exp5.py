import random
from colorama import Fore, Style, init
import matplotlib.pyplot as plt

init(autoreset=True)

comparison_count = 0
max_depth_seen = 0


def min_max_dc(arr, low, high, depth=0):
    global comparison_count, max_depth_seen
    max_depth_seen = max(max_depth_seen, depth)

    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid, depth + 1)
    rmin, rmax = min_max_dc(arr, mid + 1, high, depth + 1)

    # Conquer: 2 comparisons to combine
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin
    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax
    return overall_min, overall_max


def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


def run_analysis():
    sizes = [10, 100, 1000, 10000, 100000]
    rows = []

    print(Fore.CYAN + Style.BRIGHT +
          f"\n{'Size':>8} {'DC Comps':>10} {'Naive':>10} "
          f"{'Formula':>10} {'DC Depth':>10}")
    print(Fore.CYAN + "-" * 55)

    for size in sizes:
        global comparison_count, max_depth_seen
        arr = [random.randint(1, 10 ** 6) for _ in range(size)]

        comparison_count = 0
        max_depth_seen = 0
        min_max_dc(arr, 0, len(arr) - 1)
        dc = comparison_count
        depth = max_depth_seen

        _, _, naive = min_max_naive(arr)
        formula = 3 * size // 2 - 2

        print(f"{Fore.WHITE}{size:>8} "
              f"{Fore.GREEN}{dc:>10}{Style.RESET_ALL} "
              f"{Fore.RED}{naive:>10}{Style.RESET_ALL} "
              f"{Fore.YELLOW}{formula:>10}{Style.RESET_ALL} "
              f"{Fore.MAGENTA}{depth:>10}{Style.RESET_ALL}")
        rows.append((size, dc, naive, formula))

    return rows


def plot_results(rows):
    sizes = [r[0] for r in rows]
    dc = [r[1] for r in rows]
    naive = [r[2] for r in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, dc, marker="o", color="#2ecc71", linewidth=2,
             label="Divide & Conquer")
    plt.plot(sizes, naive, marker="s", color="#e74c3c", linewidth=2,
             label="Naive Linear Scan")
    plt.xscale("log")
    plt.xlabel("Array size (log scale)")
    plt.ylabel("Number of comparisons")
    plt.title("Min-Max: Divide & Conquer vs Naive Approach", fontweight="bold")
    plt.legend()
    plt.grid(linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("exp5_minmax_comparison.png", dpi=150)
    print(Fore.CYAN + "\nChart saved as exp5_minmax_comparison.png")


if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)
    print(Fore.CYAN + Style.BRIGHT + "  EXPERIMENT 5: MIN-MAX USING DIVIDE AND CONQUER")
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)

    demo_arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
    comparison_count = 0
    max_depth_seen = 0
    mn, mx = min_max_dc(demo_arr, 0, len(demo_arr) - 1)

    print(f"{Fore.WHITE}Array : {demo_arr}")
    print(f"{Fore.GREEN}Min = {mn}, Max = {mx}")
    print(f"{Fore.YELLOW}D&C Comparisons : {comparison_count}  "
          f"(recursion depth reached: {max_depth_seen})")

    _, _, naive_comps = min_max_naive(demo_arr)
    print(f"{Fore.RED}Naive Comparisons: {naive_comps}")

    rows = run_analysis()
    plot_results(rows)

    print(Fore.CYAN + Style.BRIGHT +
          "\nInference: Divide & Conquer needs ~3n/2 - 2 comparisons vs "
          "2(n-1) for the naive scan — a consistent ~25% reduction — while "
          "keeping recursion depth at O(log n), confirming the theoretical "
          "complexity bound.")
