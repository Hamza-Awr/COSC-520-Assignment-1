from random import choice, sample
from string import ascii_lowercase, digits

chars = ascii_lowercase + digits # random usernames

def binary_search(sorted_list, target):
    """
    Iterative binary search. Returns True if target exists in sorted_list
    """
    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return True
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

def benchmark_binary_search(n, number=1000):
    """
    Generate 'n' usernames, perform 'number' lookups (half existing, half random)
    Returns average lookup time in seconds
    """
    usernames = [''.join(choice(chars) for _ in range(5)) + str(i) for i in range(n)]
    usernames.sort()

    lookups = min(number // 2, len(usernames))
    negative_samples = number - lookups

    lookup_names = sample(usernames, lookups) + [''.join(choice(chars) for _ in range(5)) for _ in range(negative_samples)]

    import time
    start_time = time.perf_counter_ns()
    for name in lookup_names:
        binary_search(usernames, name)
    total_time = time.perf_counter_ns() - start_time

    avg_time_sec = (total_time / len(lookup_names)) / 1e9
    return avg_time_sec

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    n_list_binary = [10**3, 10**4, 10**5, 10**6, 10**7]
    times_binary = []

    for n in n_list_binary:
        avg_time = benchmark_binary_search(n)
        times_binary.append(avg_time)
        print(f"n={n}, average lookup time={avg_time:.9f} s")

    plt.plot(n_list_binary, times_binary, marker='o', color='orange')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average lookup time (s)")
    plt.title("Binary Search Average Lookup Performance")
    plt.show()
