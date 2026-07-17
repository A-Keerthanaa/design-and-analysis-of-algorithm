import random
from colorama import Fore, Style, init
import matplotlib.pyplot as plt

init(autoreset=True)


def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)
    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q
    return matches, comparisons


def print_table(patterns, results):
    print(Fore.CYAN + Style.BRIGHT +
          f"\n{'Pattern':>12} {'Naive':>10} {'KMP':>10} {'RK':>10}")
    print(Fore.CYAN + "-" * 46)
    for p, (c1, c2, c3) in zip(patterns, results):
        print(f"{Fore.WHITE}{p:>12} "
              f"{Fore.RED}{c1:>10}{Style.RESET_ALL} "
              f"{Fore.GREEN}{c2:>10}{Style.RESET_ALL} "
              f"{Fore.YELLOW}{c3:>10}{Style.RESET_ALL}")


def plot_pattern_comparison(patterns, results):
    naive = [r[0] for r in results]
    kmp   = [r[1] for r in results]
    rk    = [r[2] for r in results]

    x = range(len(patterns))
    width = 0.25
    plt.figure(figsize=(8, 5))
    plt.bar([i - width for i in x], naive, width, label="Naive", color="#e74c3c")
    plt.bar(x, kmp, width, label="KMP", color="#2ecc71")
    plt.bar([i + width for i in x], rk, width, label="Rabin-Karp", color="#3498db")
    plt.xticks(list(x), patterns)
    plt.ylabel("Character comparisons")
    plt.title("String Matching Comparison by Pattern (text length 10000)")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("exp2_pattern_comparison.png", dpi=150)
    print(Fore.CYAN + "\nChart saved as exp2_pattern_comparison.png")


def plot_scaling_by_text_size():
    """How each algorithm scales as the TEXT length grows (fixed pattern)."""
    sizes = [1000, 5000, 10000, 15000, 20000]
    pattern = "ABCDAB"
    naive_counts, kmp_counts, rk_counts = [], [], []

    random.seed(7)
    for size in sizes:
        text = "".join(random.choices("ABCD", k=size))
        _, n1 = naive_search(text, pattern)
        _, n2 = kmp_search(text, pattern)
        _, n3 = rabin_karp(text, pattern)
        naive_counts.append(n1)
        kmp_counts.append(n2)
        rk_counts.append(n3)

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, naive_counts, marker="o", color="#e74c3c", label="Naive")
    plt.plot(sizes, kmp_counts, marker="s", color="#2ecc71", label="KMP")
    plt.plot(sizes, rk_counts, marker="^", color="#3498db", label="Rabin-Karp")
    plt.xlabel("Text length (characters)")
    plt.ylabel("Character comparisons")
    plt.title(f"Scaling with Text Size (pattern = '{pattern}')")
    plt.legend()
    plt.grid(linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("exp2_scaling_by_textsize.png", dpi=150)
    print(Fore.CYAN + "Chart saved as exp2_scaling_by_textsize.png")


if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)
    print(Fore.CYAN + Style.BRIGHT + "  EXPERIMENT 2: STRING MATCHING ALGORITHMS")
    print(Fore.CYAN + Style.BRIGHT + "=" * 65)

    text = "AABAACAADAABAABA"
    pattern = "AABA"
    print(f"{Fore.WHITE}Text   : {text}")
    print(f"{Fore.WHITE}Pattern: {pattern}\n")

    m1, c1 = naive_search(text, pattern)
    m2, c2 = kmp_search(text, pattern)
    m3, c3 = rabin_karp(text, pattern)

    print(f"{Fore.RED}Naive      -> Matches: {m1}, Comparisons: {c1}")
    print(f"{Fore.GREEN}KMP        -> Matches: {m2}, Comparisons: {c2}")
    print(f"{Fore.YELLOW}Rabin-Karp -> Matches: {m3}, Comparisons: {c3}")

    # Performance comparison on a larger random text
    random.seed(42)
    text_large = "".join(random.choices("ABCD", k=10000))
    patterns = ["AB", "ABCD", "ABCDAB", "ABCDABCD"]
    results = []
    for p in patterns:
        _, n1 = naive_search(text_large, p)
        _, n2 = kmp_search(text_large, p)
        _, n3 = rabin_karp(text_large, p)
        results.append((n1, n2, n3))

    print_table(patterns, results)
    plot_pattern_comparison(patterns, results)
    plot_scaling_by_text_size()

    print(Fore.CYAN + Style.BRIGHT +
          "\nInference: KMP guarantees O(n+m) comparisons irrespective of "
          "pattern content, since it never re-examines a matched prefix. "
          "Rabin-Karp's rolling hash keeps comparisons low by filtering out "
          "most non-matching windows before doing a full character check. "
          "Naive search degrades the most as pattern length and text size "
          "grow, confirming its O(nm) worst case.")
