import time
import random
from colorama import Fore, Style, init
import matplotlib.pyplot as plt

init(autoreset=True)  # colorama auto-reset after every print


def interpolation_search(arr, target):
    """
    Interpolation Search.
    Time Complexity : O(log log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        # Probe position estimated using the interpolation formula
        pos = low + int(((target - arr[low]) * (high - low))
                         / (arr[high] - arr[low]))

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def binary_search(arr, target):
    """Classic Binary Search — O(log n)."""
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


def colored_row(size, is_t, bs_t, is_c, bs_c):
    return (f"{Fore.CYAN}{size:>10}{Style.RESET_ALL} "
            f"{Fore.GREEN}{is_t:>12.4f}{Style.RESET_ALL} "
            f"{Fore.YELLOW}{bs_t:>12.4f}{Style.RESET_ALL} "
            f"{Fore.GREEN}{is_c:>10}{Style.RESET_ALL} "
            f"{Fore.YELLOW}{bs_c:>10}{Style.RESET_ALL}")


def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []

    print(Fore.CYAN + Style.BRIGHT +
          f"\n{'Size':>10} {'IS(ms)':>12} {'BS(ms)':>12} "
          f"{'IS_cmp':>10} {'BS_cmp':>10}")
    print(Fore.CYAN + "-" * 58)

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(50):
            _, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 50 * 1000

        start = time.perf_counter()
        for _ in range(50):
            _, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 50 * 1000

        print(colored_row(size, is_time, bs_time, comp_is, comp_bs))
        results.append((size, is_time, bs_time, comp_is, comp_bs))

    return results


def plot_results(results):
    sizes  = [r[0] for r in results]
    is_t   = [r[1] for r in results]
    bs_t   = [r[2] for r in results]
    is_cmp = [r[3] for r in results]
    bs_cmp = [r[4] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Interpolation Search vs Binary Search", fontsize=14,
                 fontweight="bold")

    # --- Chart 1: comparisons
    width = 0.35
    x = range(len(sizes))
    ax1.bar([i - width / 2 for i in x], is_cmp, width=width,
            label="Interpolation", color="#2ecc71")
    ax1.bar([i + width / 2 for i in x], bs_cmp, width=width,
            label="Binary", color="#f1c40f")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(sizes)
    ax1.set_xlabel("Array size")
    ax1.set_ylabel("Comparisons")
    ax1.set_title("Number of comparisons")
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # --- Chart 2: timing lines
    ax2.plot(sizes, is_t, marker="o", color="#2ecc71", label="Interpolation")
    ax2.plot(sizes, bs_t, marker="s", color="#f1c40f", label="Binary")
    ax2.set_xlabel("Array size")
    ax2.set_ylabel("Time (ms)")
    ax2.set_title("Average search time")
    ax2.legend()
    ax2.grid(linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("exp1_search_comparison.png", dpi=150)
    print(Fore.CYAN + "\nChart saved as exp1_search_comparison.png")


if __name__ == "__main__":
    arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]
    target = 35

    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "  EXPERIMENT 1: INTERPOLATION SEARCH")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

    idx, comps = interpolation_search(arr, target)
    print(f"{Fore.WHITE}Array   : {arr}")
    print(f"{Fore.WHITE}Target  : {target}")
    print(f"{Fore.GREEN}Found at index {idx} using {comps} comparisons"
          f"{Style.RESET_ALL}")

    data = performance_analysis()
    plot_results(data)

    print(Fore.CYAN + Style.BRIGHT +
          "\nInference: Interpolation Search consistently needs fewer "
          "comparisons than Binary Search on large, uniformly distributed "
          "data, approaching O(log log n) versus O(log n).")
